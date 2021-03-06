package com.daw48.detector;

import com.intellij.openapi.application.WriteAction;
import com.intellij.openapi.vfs.VfsUtil;
import com.intellij.openapi.vfs.VirtualFile;

import java.io.IOException;
import java.util.Objects;

/**
 * @author Darren S. White
 */
public class ExternalDetectionTest extends BaseTest {
    /**
     * The filename to test
     */
    private static final String filename = "file.txt";
    /**
     * The initial content of the file
     */
    private static final String initialContent = "Initial content";
    /**
     * The external content to add
     */
    private static final String externalContent = "\nExternal content";
    /**
     * The file to test
     */
    private VirtualFile file;

    @Override
    protected void setUp() throws Exception {
        super.setUp();
        file = createFile(filename, initialContent);
    }

    /**
     * Test for detecting external changes
     */
    public void testExternalChangeDetection() throws IOException {
        ProjectDocumentListener listener =
                ProjectDocumentListener.getInstance(getProject());

        try {
            // Simulate closing the project
            // If we actually close the project then we can't write to the file
            listener.projectClosed();

            // Append the external content
            WriteAction.run(() -> VfsUtil.saveText(file,
                    initialContent + externalContent));
        } finally {
            // Re-open the project
            listener.projectOpened();
        }

        // Check the tracked changes
        assertChangeListSize(filename, 3);
        assertOneChangeMatches(filename, (c) -> c.source == Change.Source.EXTERNAL
                && Objects.equals(c.oldString, "")
                && Objects.equals(c.newString, externalContent)
                && c.offset == 15);
    }
}
