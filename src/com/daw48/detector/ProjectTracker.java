package com.daw48.detector;

import com.intellij.openapi.components.*;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.ide.CopyPasteManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.util.xmlb.XmlSerializerUtil;
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
        storages = @Storage(StoragePathMacros.WORKSPACE_FILE))
public class ProjectTracker implements
        PersistentStateComponent<ProjectTracker> {
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
    public Map<String, FileTracker> files = new HashMap<>();

    private void addChange(VirtualFile file, DocumentEvent event,
                           Change.Source source) {
        if (file == null || file.getCanonicalPath() == null) {
            return;
        }
        String path = file.getCanonicalPath();
        Change change = new Change(event.getOffset(),
                event.getOldFragment().toString(),
                event.getNewFragment().toString(), source,
                System.currentTimeMillis());
        FileTracker tracker = files.getOrDefault(path, new FileTracker(path));

        LOG.info("File changed: " + path);

        tracker.addChange(change, event.getDocument().getText());
        files.put(path, tracker);
    }

    private boolean detectCopyPaste(DocumentEvent event) {
        String newFragment = event.getNewFragment().toString().trim();
        for (Transferable t : CopyPasteManager.getInstance().getAllContents()) {
            String content = getTransferableString(t);
            if (content != null && newFragment.equals(content.trim())) {
                LOG.warn("Copy-paste detected: " + content);
                return true;
            }
        }
        return false;
    }

    public static ProjectTracker getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, ProjectTracker.class);
    }

    @Nullable
    @Override
    public ProjectTracker getState() {
        return this;
    }

    private static String getTransferableString(Transferable content) {
        try {
            return content == null ? null :
                    (String) content.getTransferData(DataFlavor.stringFlavor);
        } catch (IOException | UnsupportedFlavorException e) {
            return null;
        }
    }

    @Override
    public void loadState(@NotNull ProjectTracker state) {
        XmlSerializerUtil.copyBean(state, this);
    }

    public void processDocumentEvent(DocumentEvent event) {
        Document doc = event.getDocument();
        VirtualFile file = FileDocumentManager.getInstance().getFile(doc);
        Change.Source source;

        assert file != null;

        if (detectCopyPaste(event)) {
            source = Change.Source.CLIPBOARD;
        } else {
            source = Change.Source.OTHER;
        }

        addChange(file, event, source);
    }
}
