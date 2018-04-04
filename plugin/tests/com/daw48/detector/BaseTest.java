package com.daw48.detector;

import com.intellij.openapi.application.WriteAction;
import com.intellij.openapi.vfs.VfsUtil;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.testFramework.VfsTestUtil;
import com.intellij.testFramework.fixtures.LightPlatformCodeInsightFixtureTestCase;
import org.junit.Assert;

import java.io.IOException;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Predicate;

/**
 * Common class used for tests
 *
 * @author Darren S. White
 */
public abstract class BaseTest extends LightPlatformCodeInsightFixtureTestCase {
    /**
     * Files used during tests which should be closed in tearDown
     */
    private final Set<VirtualFile> tearDownFiles = new HashSet<>();

    /**
     * Asserts that the file has a given number of changes
     *
     * @param path The path of the file to check the changes for
     * @param size The number of changes to assert
     */
    public void assertChangeListSize(String path, int size) {
        assertEquals(size, changesForFile(path).size());
    }

    /**
     * Asserts that the file has a tracked changed
     *
     * @param path      The path of the file to check changes for
     * @param predicate Tests a change
     */
    public void assertOneChangeMatches(String path,
                                       Predicate<Change> predicate) {
        List<Change> changes = changesForFile(path);
        boolean found = false;

        for (Change c : changes) {
            if (predicate.test(c)) {
                found = true;
                break;
            }
        }

        Assert.assertTrue(predicate + " did not match one of " +
                changes.toString(), found);
    }

    /**
     * Gets the change list for a file
     *
     * @param path The path of the file to get the changes for
     * @return A List of changes
     */
    public List<Change> changesForFile(String path) {
        ProjectTracker tracker = ProjectTracker.getInstance(getProject());
        if (tracker.files.containsKey(path)) {
            return tracker.files.get(path).changes;
        } else {
            return Collections.emptyList();
        }
    }

    /**
     * Create a file with the given name
     *
     * @param filename The name of the file to create
     * @return A VirtualFile pointing to the filename
     */
    public VirtualFile createFile(String filename) {
        return createFile(filename, "", true, true);
    }

    /**
     * Create a file with the given name and content
     *
     * @param filename The name of the file to create
     * @param content  The initial content of the file
     * @return A VirtualFile pointing to the filename with the content
     */
    public VirtualFile createFile(String filename, String content) {
        return createFile(filename, content, true, true);
    }

    /**
     * Create a file with the given name
     *
     * @param filename         The name of the file to create
     * @param configure        true if the file should be configured for the test; false otherwise
     * @param deleteOnTearDown If the file should be deleted in tearDown
     * @return A VirtualFile pointing to the filename
     */
    public VirtualFile createFile(String filename, boolean configure,
                                  boolean deleteOnTearDown) {
        return createFile(filename, "", configure, deleteOnTearDown);
    }

    /**
     * Create a file with the given name and content
     *
     * @param filename         The name of the file to create
     * @param content          The initial content of the file
     * @param configure        true if the file should be configured for the test; false otherwise
     * @param deleteOnTearDown If the file should be deleted in tearDown
     * @return A VirtualFile pointing to the filename
     */
    public VirtualFile createFile(String filename, String content,
                                  boolean configure, boolean deleteOnTearDown) {
        // Create the file in the project directory
        VirtualFile file = VfsTestUtil.createFile(getProject().getBaseDir(),
                filename, content);

        // Load the file into the in-memory editor
        if (configure) {
            myFixture.configureFromExistingVirtualFile(file);

            // Write the content again to trigger file tracking
            WriteAction.run(() -> {
                try {
                    VfsUtil.saveText(file, content);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        }

        // Delete the file after the test
        if (deleteOnTearDown) {
            tearDownFiles.add(file);
        }

        return file;
    }

    @Override
    protected void tearDown() throws Exception {
        // Ensure tracked files do not persist between tests
        ProjectTracker.getInstance(getProject()).files.clear();
        // Delete all files that were created (and requested to be deleted)
        for (VirtualFile f : tearDownFiles) {
            VfsTestUtil.deleteFile(f);
        }
        super.tearDown();
    }
}
