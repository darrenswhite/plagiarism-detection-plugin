package com.daw48.detector;

import com.intellij.testFramework.fixtures.LightPlatformCodeInsightFixtureTestCase;
import org.junit.Assert;

import java.util.Collections;
import java.util.List;
import java.util.function.Predicate;

/**
 * Common class used for tests
 *
 * @author Darren S. White
 */
public abstract class BaseTest extends LightPlatformCodeInsightFixtureTestCase {
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

    @Override
    protected void tearDown() throws Exception {
        ProjectTracker.getInstance(getProject()).files.clear();
        super.tearDown();
    }
}