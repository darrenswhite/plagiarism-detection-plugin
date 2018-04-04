package com.daw48.detector;

import com.intellij.designer.clipboard.SimpleTransferable;
import com.intellij.ide.CopyPasteManagerEx;
import com.intellij.openapi.actionSystem.IdeActions;
import com.intellij.openapi.vfs.VirtualFile;

import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.util.Objects;

/**
 * @author Darren S. White
 */
public class CopyPasteDetectionTest extends BaseTest {
    /**
     * The filename to test
     */
    private static final String filename = "file.txt";
    /**
     * The clipboard contents to test
     */
    private static final String content = "A small string";
    /**
     * Clipboard value to paste
     */
    private static final Transferable transferableContent = new SimpleTransferable(
            content, DataFlavor.stringFlavor);
    /**
     * The file to test with
     */
    private VirtualFile file;

    @Override
    protected void setUp() throws Exception {
        super.setUp();
        file = createFile(filename);
    }

    @Override
    protected void tearDown() throws Exception {
        // Remove the clipboard content
        CopyPasteManagerEx.getInstanceEx().removeContent(transferableContent);
        super.tearDown();
    }

    /**
     * Test for detecting copy-paste
     */
    public void testCopyPasteDetection() {
        // Set the clipboard content
        CopyPasteManagerEx.getInstanceEx().setContents(transferableContent);

        // Paste contents
        myFixture.performEditorAction(IdeActions.ACTION_EDITOR_PASTE);

        // Check the tracked changes
        assertChangeListSize(file.getPath(), 2);
        assertOneChangeMatches(file.getPath(), (c) ->
                c.source == Change.Source.CLIPBOARD
                        && Objects.equals(c.oldString, "")
                        && Objects.equals(c.newString, content)
                        && c.offset == 0);
    }
}
