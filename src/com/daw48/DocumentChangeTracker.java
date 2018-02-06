package com.daw48;

import com.intellij.openapi.components.ProjectComponent;
import com.intellij.openapi.components.ServiceManager;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.EditorFactory;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.editor.event.DocumentListener;
import com.intellij.openapi.ide.CopyPasteManager;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.io.IOException;

public class DocumentChangeTracker implements DocumentListener, ProjectComponent {
    private static final Logger LOG = Logger.getInstance(DocumentChangeTracker.class);
    private final Project project;

    public DocumentChangeTracker(@NotNull Project project) {
        this.project = project;
    }

    @Override
    public void documentChanged(DocumentEvent event) {
        String newFragment = event.getNewFragment().toString().trim();

        LOG.info(event.toString());

        for (Transferable t : CopyPasteManager.getInstance().getAllContents()) {
            String content = getTransferableString(t);
            if (content == null) {
                continue;
            }
            if (newFragment.equals(content.trim())) {
                LOG.warn("COPY-PASTE DETECTED: " + content);
            }
        }
    }

    public static DocumentChangeTracker getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, DocumentChangeTracker.class);
    }

    @Override
    public void projectClosed() {
        EditorFactory.getInstance().getEventMulticaster()
                .removeDocumentListener(this);
    }

    @Override
    public void projectOpened() {
        EditorFactory.getInstance().getEventMulticaster()
                .addDocumentListener(this, project);
    }

    private static String getTransferableString(Transferable content) {
        try {
            return content == null ? null :
                    (String) content.getTransferData(DataFlavor.stringFlavor);
        } catch (IOException | UnsupportedFlavorException e) {
            return null;
        }
    }
}
