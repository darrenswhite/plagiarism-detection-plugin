package com.daw48.detector;

import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.testFramework.VfsTestUtil;

import java.io.IOException;
import java.util.Objects;

/**
 * @author Darren S. White
 */
public class ExternalDetectionTest extends BaseTest {

    /**
     * Test for detecting external changes
     */
    public void testExternalChangeDetection() {
        String filename = "file.txt";
        String initialContent = "Initial content";
        String externalContent = "\nExternal content";
        VirtualFile file = VfsTestUtil.createFile(getProject().getBaseDir(),
                filename, initialContent);

        myFixture.configureFromExistingVirtualFile(file);

        ApplicationManager.getApplication().runWriteAction(() -> {
            try {
                file.setBinaryContent(initialContent.getBytes());
            } catch (IOException e) {
                e.printStackTrace();
                fail("Failed to write initial content");
            }
        });

        ProjectDocumentListener listener =
                ProjectDocumentListener.getInstance(getProject());

        listener.projectClosed();

        ApplicationManager.getApplication().runWriteAction(() -> {
            try {
                file.setBinaryContent((initialContent + externalContent).getBytes());
            } catch (IOException e) {
                e.printStackTrace();
                fail("Failed to write external content");
            }
        });

        listener.projectOpened();

        // Check the tracked changes
        assertChangeListSize(file.getPath(), 2);
        assertOneChangeMatches(file.getPath(), (c) -> c.source == Change.Source.EXTERNAL
                && Objects.equals(c.oldString, "")
                && Objects.equals(c.newString, externalContent)
                && c.offset == 15);
    }
}
