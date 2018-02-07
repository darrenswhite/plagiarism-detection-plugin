package com.daw48;

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
import java.util.LinkedList;
import java.util.List;

/**
 * A class used to track changes for a Document. The changes are stored in
 * the workspace file for persistence.
 *
 * @author Darren S. White
 */
@State(name = "PlagiarismDetectorProjectComponent",
        storages = @Storage(StoragePathMacros.WORKSPACE_FILE))
public class ChangeTracker implements PersistentStateComponent<ChangeTracker> {
    /**
     * The Logger for this class
     */
    private static final Logger LOG = Logger.getInstance(ChangeTracker.class);

    /**
     * The List of Changes for this Project
     * <p>
     * Keep public and non-final for serialisation
     */
    public List<Change> changes = new LinkedList<>();

    private void addChange(VirtualFile file, DocumentEvent event,
                           Change.Source source) {
        if (file == null || file.getCanonicalPath() == null) {
            return;
        }
        Change change = new Change(file.getCanonicalPath(), event.getOffset(),
                event.getOldFragment().toString(),
                event.getNewFragment().toString(), source,
                System.currentTimeMillis());
        LOG.info("Adding change: " + change.toString());
        changes.add(change);
        LOG.info("Current change set: " + changes.toString());
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

    public static ChangeTracker getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, ChangeTracker.class);
    }

    @Nullable
    @Override
    public ChangeTracker getState() {
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
    public void loadState(@NotNull ChangeTracker state) {
        XmlSerializerUtil.copyBean(state, this);
    }

    public void processDocumentEvent(DocumentEvent event) {
        final Document doc = event.getDocument();
        final VirtualFile file = FileDocumentManager.getInstance().getFile(doc);
        final Change.Source source;

        assert file != null;

        if (detectCopyPaste(event)) {
            source = Change.Source.CLIPBOARD;
        } else {
            source = Change.Source.OTHER;
        }

        addChange(file, event, source);
    }
}
