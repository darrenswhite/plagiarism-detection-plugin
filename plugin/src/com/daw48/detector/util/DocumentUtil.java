package com.daw48.detector.util;

import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.vfs.VirtualFile;

/**
 * Useful Document methods
 *
 * @author Darren S. White
 */
public class DocumentUtil {
    /**
     * Get the VirtualFile from a DocumentEvent
     *
     * @param event The DocumentEvent to get the file for
     * @return A VirtualFile for the DocumentEvent
     */
    public static VirtualFile getVirtualFile(DocumentEvent event) {
        return FileDocumentManager.getInstance().getFile(event.getDocument());
    }
}
