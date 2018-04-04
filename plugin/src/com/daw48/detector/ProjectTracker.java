package com.daw48.detector;

import com.daw48.detector.util.CipherUtil;
import com.daw48.detector.util.DocumentUtil;
import com.intellij.openapi.components.PersistentStateComponent;
import com.intellij.openapi.components.ServiceManager;
import com.intellij.openapi.components.State;
import com.intellij.openapi.components.Storage;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.ide.CopyPasteManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VfsUtil;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * A class used to track changes for a Document. The changes are stored in
 * the workspace file for persistence.
 *
 * @author Darren S. White
 */
@State(name = "PlagiarismDetectorProjectComponent",
        storages = @Storage("plagiarism_detection.xml"))
public class ProjectTracker implements
        PersistentStateComponent<ProjectTracker.CipherState> {
    /**
     * The Logger for this class
     */
    private static final Logger LOG = Logger.getInstance(ProjectTracker.class);
    /**
     * The Map of FileChanges for this Project
     * <p>
     * The key is the file path
     * <p>
     * Keep public and non-final for serialisation
     */
    public final Map<String, FileTracker> files = new HashMap<>();
    /**
     * The current open project
     */
    private final Project project;

    /**
     * Creates a new ProjectTracker
     *
     * @param project The Project to track
     */
    public ProjectTracker(Project project) {
        this.project = project;
    }

    /**
     * Gets the current instance for this class for a given Project
     *
     * @param project The current Project
     * @return A ProjectTracker instance
     */
    public static ProjectTracker getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, ProjectTracker.class);
    }

    /**
     * Gets the String representation for a Transferable object
     *
     * @param content The Transferable object to convert to a String
     * @return A String representation for the given Transferable
     */
    private static String getTransferableString(Transferable content) {
        try {
            return content == null ? null :
                    (String) content.getTransferData(DataFlavor.stringFlavor);
        } catch (IOException | UnsupportedFlavorException e) {
            return null;
        }
    }

    /**
     * Add a change with a given Source from a DocumentEvent for a particular
     * file
     *
     * @param file   The file which changed
     * @param event  The DocumentEvent that was fired
     * @param source The Source of the change
     */
    private void addChange(VirtualFile file, DocumentEvent event,
                           Change.Source source) {
        if (file == null || file.getParent() == null) {
            return;
        }

        // Use relative paths
        String path = VfsUtil.getRelativePath(file, project.getBaseDir());
        Change change = new Change(event.getOffset(),
                event.getOldFragment().toString(),
                event.getNewFragment().toString(), source,
                System.currentTimeMillis());
        FileTracker tracker = files.getOrDefault(path, new FileTracker(path));

        LOG.info("File changed: " + path);

        // If file isn't tracked, check if it already has contents
        if (!files.containsKey(path)) {
            String content = event.getDocument().getText();
            // Remove the current change
            content = content.substring(0, event.getOffset()) +
                    content.substring(event.getOffset() + event.getNewLength());
            // If the content is not empty it still has content
            if (!content.isEmpty()) {
                LOG.info("Previous content detected: " + content);
                tracker.addChange(new Change(0, "", content, Change.Source.EXTERNAL,
                        System.currentTimeMillis()), content.getBytes());
            }
        }

        tracker.addChange(change, event.getDocument().getText().getBytes());
        files.put(path, tracker);
    }

    /**
     * Checks if a DocumentEvent was actually copy-paste
     *
     * @param event The DocumentEvent to check
     * @return <tt>true</tt> if the DocumentEvent was copy-paste; <tt>false</tt>
     * otherwise
     */
    private boolean detectCopyPaste(DocumentEvent event) {
        String newFragment = event.getNewFragment().toString().trim();
        // Compare the fragment with all clipboard contents
        for (Transferable t : CopyPasteManager.getInstance().getAllContents()) {
            String content = getTransferableString(t);
            if (content != null && newFragment.equals(content.trim())) {
                LOG.warn("Copy-paste detected: " + content);
                return true;
            }
        }
        return false;
    }

    @Nullable
    @Override
    public CipherState getState() {
        CipherState state = new CipherState();

        // Encrypte the tracked data
        state.files.putAll(CipherUtil.cipher(files));

        return state;
    }

    @Override
    public void loadState(@NotNull CipherState state) {
        files.clear();
        // Decrypt the tracked data
        files.putAll(CipherUtil.decipher(state.files, FileTracker.class));
        LOG.info("Loaded state: " + files);
    }

    /**
     * Process a DocumentEvent that was fired from a DocumentListener
     * <p>
     * This will detect the source of the event and track the change
     *
     * @param event The DocumentEvent to process
     */
    public void processDocumentEvent(DocumentEvent event) {
        VirtualFile file = DocumentUtil.getVirtualFile(event);
        Change.Source source;

        if (file == null) {
            return;
        }

        if (detectCopyPaste(event)) {
            source = Change.Source.CLIPBOARD;
        } else {
            source = Change.Source.OTHER;
        }

        addChange(file, event, source);
    }

    /**
     * Encrypted persistent state
     */
    static class CipherState {
        /**
         * Map of encrypted file data
         */
        public Map<String, String> files = new HashMap<>();
    }
}
