package com.daw48.detector;

import com.daw48.detector.util.DocumentUtil;
import com.daw48.detector.util.RefactoringData;
import com.intellij.diff.comparison.ComparisonManagerImpl;
import com.intellij.diff.comparison.ComparisonPolicy;
import com.intellij.diff.fragments.DiffFragment;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.components.ProjectComponent;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.EditorFactory;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.editor.event.DocumentListener;
import com.intellij.openapi.progress.util.ProgressIndicatorBase;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.refactoring.listeners.RefactoringEventData;
import com.intellij.refactoring.listeners.RefactoringEventListener;
import org.apache.commons.compress.utils.IOUtils;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.io.IOException;
import java.util.*;

/**
 * This class listens for changes in a Document per Project
 *
 * @author Darren S. White
 */
public class ProjectDocumentListener implements DocumentListener,
        ProjectComponent, RefactoringEventListener {
    /**
     * The Logger for this class
     */
    private static final Logger LOG = Logger
            .getInstance(ProjectDocumentListener.class);

    /**
     * The current Project
     */
    private final Project project;

    /**
     * The tracker for all of the Changes
     */
    private final ProjectTracker tracker;

    /**
     * The current/last refactoring data
     */
    private RefactoringData refactoringData;

    /**
     * Create a new ProjectDocumentListener
     *
     * @param project The current Project
     */
    public ProjectDocumentListener(@NotNull Project project) {
        this.project = project;
        this.tracker = ProjectTracker.getInstance(project);
    }

    /**
     * Gets the current instance for this class
     *
     * @return A ProjectDocumentListener instance
     */
    public static ProjectDocumentListener getInstance(@NotNull Project project) {
        return project.getComponent(ProjectDocumentListener.class);
    }

    /**
     * Checks if any of the tracked files were changed externally
     * <p>
     * This works by comparing the base64 encoded cache for each file against
     * its current base64 encoded content
     */
    private void checkCachedExternalChanges() {
        // Check all tracked files
        for (Map.Entry<String, FileTracker> entry : tracker.files.entrySet()) {
            String path = entry.getKey();
            FileTracker tracker = entry.getValue();
            VirtualFile file = project.getBaseDir()
                    .findFileByRelativePath(path);

            if (file == null) {
                continue;
            }

            try {
                String cachedContent = new String(Base64.getDecoder()
                        .decode(entry.getValue().cache));

                // Ensure the file is up-to-date with the file system
                file.refresh(false, false);

                if (file.exists()) {
                    String newContent = new String(IOUtils.toByteArray(
                            file.getInputStream()));

                    // Compare cache with current data
                    if (!Objects.equals(cachedContent, newContent)) {
                        LOG.warn("File changed externally: " + path);
                        List<Change> changes = getChanges(cachedContent,
                                newContent);
                        for (Change c : changes) {
                            tracker.addChange(c, newContent.getBytes());
                        }
                    }
                } else {
                    LOG.warn("File removed externally: " + path);
                    Change change = new Change(0, cachedContent, "",
                            Change.Source.EXTERNAL,
                            System.currentTimeMillis());
                    // File was removed so cache is null
                    tracker.addChange(change, null);
                }
            } catch (IOException e) {
                LOG.warn("Unable to check external changes: " + path, e);
            }
        }
    }

    @Override
    public void documentChanged(DocumentEvent event) {
        VirtualFile file = DocumentUtil.getVirtualFile(event);
        // Don't track .idea directory
        if (file != null && !file.getPath().contains(".idea/")) {
            // Track the change
            tracker.processDocumentEvent(event);
        }
    }

    /**
     * Get all changes from the diff between cache and new content
     *
     * @param cachedContent The cache content String
     * @param newContent    The new content String to compare against
     * @return A List of Change's
     */
    private List<Change> getChanges(String cachedContent, String newContent) {
        List<Change> changes = new ArrayList<>();
        // Get the list of diffs
        List<DiffFragment> fragments = ComparisonManagerImpl.getInstanceImpl()
                .compareChars(cachedContent, newContent,
                        ComparisonPolicy.DEFAULT, new ProgressIndicatorBase());

        // Convert diffs to changes
        for (DiffFragment f : fragments) {
            if (f.getStartOffset1() != f.getStartOffset2()) {
                LOG.warn("DiffFragment has different start offsets: " +
                        f.toString());
            }
            int offset = f.getStartOffset1();
            String oldString = cachedContent.substring(f.getStartOffset1(), f.getEndOffset1());
            String newString = newContent.substring(f.getStartOffset2(), f.getEndOffset2());
            changes.add(new Change(offset, oldString, newString,
                    Change.Source.EXTERNAL, System.currentTimeMillis()));
        }

        return changes;
    }

    @Override
    public void projectClosed() {
        EditorFactory.getInstance().getEventMulticaster()
                .removeDocumentListener(this);
    }

    @Override
    public void projectOpened() {
        ApplicationManager.getApplication().runReadAction(this::checkCachedExternalChanges);
        EditorFactory.getInstance().getEventMulticaster()
                .addDocumentListener(this, project);
        project.getMessageBus().connect().subscribe(RefactoringEventListener.REFACTORING_EVENT_TOPIC, this);
    }

    @Override
    public void refactoringStarted(@NotNull String refactoringId, @Nullable RefactoringEventData beforeData) {
        LOG.info("Refactoring started: " + refactoringId);

        refactoringData = new RefactoringData(refactoringId);

        if (beforeData != null) {
            refactoringData.setBeforeData(beforeData);
        }
    }

    @Override
    public void refactoringDone(@NotNull String refactoringId, @Nullable RefactoringEventData afterData) {
        LOG.info("Refactoring done: " + refactoringId);
        if (afterData != null && refactoringData != null) {
            refactoringData.setAfterData(afterData);
            refactoringData.execute(tracker);
        }
    }

    @Override
    public void conflictsDetected(@NotNull String refactoringId, @NotNull RefactoringEventData conflictsData) {
        LOG.info("Refactoring conflictsData detection: " + refactoringId);
        if (refactoringData != null) {
            refactoringData.setConflictsData(conflictsData);
        }
    }

    @Override
    public void undoRefactoring(@NotNull String refactoringId) {
        LOG.info("Undo refactoring: " + refactoringId);
        refactoringData.undo(tracker);
    }
}
