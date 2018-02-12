package com.daw48.detector;

import com.intellij.designer.clipboard.SimpleTransferable;
import com.intellij.openapi.actionSystem.IdeActions;
import com.intellij.openapi.ide.CopyPasteManager;
import com.intellij.openapi.vfs.VirtualFile;

import java.awt.datatransfer.DataFlavor;
import java.util.Objects;

/**
 * @author Darren S. White
 */
public class CopyPasteDetectionTest extends BaseTest {

    /**
     * Test for detecting copy-paste
     */
    public void testCopyPasteDetection() {
        String filename = "file.txt";
        String content = "A small string";
        VirtualFile file = myFixture.getTempDirFixture().createFile(filename);

        // Setup the test file
        myFixture.configureByFile(filename);

        // Set the clipboard content
        CopyPasteManager.getInstance().setContents(new SimpleTransferable(
                content, DataFlavor.stringFlavor));

        // Paste contents
        myFixture.performEditorAction(IdeActions.ACTION_EDITOR_PASTE);

        // Check the tracked changes
        assertChangeListSize(file.getPath(), 1);
        assertOneChangeMatches(file.getPath(), (c) ->
                c.source == Change.Source.CLIPBOARD
                        && Objects.equals(c.oldString, "")
                        && Objects.equals(c.newString, content));
    }
}
