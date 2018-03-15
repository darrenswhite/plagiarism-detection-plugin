package com.daw48.detector;

import com.intellij.openapi.vfs.VirtualFile;

import java.util.Objects;

/**
 * @author Darren S. White
 */
public class CodeGenerationDetectionTest extends BaseTest {

    private static final String filename = "file.txt";
    private static final String content = "Automatic code generation test";

    private VirtualFile file;

    @Override
    protected void setUp() throws Exception {
        super.setUp();
        file = createFile(filename);
    }

    /**
     * Test for detecting code generation
     */
    public void testCodeGenerationDetection() {

    }
}
