package com.daw48.detector.util;

import com.daw48.detector.FileTracker;
import com.daw48.detector.ProjectTracker;
import com.intellij.psi.PsiClass;
import com.intellij.psi.PsiElement;
import com.intellij.refactoring.listeners.RefactoringEventData;

/**
 * Wrapper for RefactoringEventData to perform refactoring methods
 *
 * Adds/removes changes to ProjectTracker when refactoring is done/undone
 *
 * @author Darren S. White
 */
public class RefactoringData {
    /**
     * The id of the refactoring method
     */
    private final String id;

    /**
     * The data before refactoring was performed
     */
    private RefactoringEventData beforeData;

    /**
     * The data after refactoring was performed
     */
    private RefactoringEventData afterData;

    /**
     * The data if conflicts occur during refactoring
     */
    private RefactoringEventData conflictsData;

    /**
     * The path of the file before refactoring was performed
     */
    private String beforePath;

    /**
     * The path of the file after refactoring was performed
     */
    private String afterPath;

    /**
     * Create a new RefactoringData object with the id
     *
     * @param id The refactoring method id
     */
    public RefactoringData(String id) {
        this.id = id;

    }

    /**
     * Perform the refactoring method. This is dependant on the refactoring id.
     * @param tracker The ProjectTracker to add the changes to
     */
    public void execute(ProjectTracker tracker) {
        switch (id) {
            case "refactoring.rename":
                executeRename(tracker, false);
                break;
        }
    }

    /**
     * Perform file rename refactoring
     *
     * @param tracker The ProjectTracker to add the changes to
     * @param undo true if refactoring is being undone; false otherwise
     */
    private void executeRename(ProjectTracker tracker, boolean undo) {
        // Only file/class renaming is currently supported
        if (getPsiElement(beforeData) instanceof PsiClass) {
            // Swap the paths for undo
            String beforePath = undo ? this.afterPath : this.beforePath;
            String afterPath = undo ? this.beforePath : this.afterPath;
            // Move the changes to the new path
            if (tracker.files.containsKey(beforePath)) {
                FileTracker ft = tracker.files.remove(beforePath);
                ft.path = afterPath;
                tracker.files.put(afterPath, ft);
            }
        }
    }

    /**
     * Get the file path for the given RefactoringEventData
     *
     * @param data The data to get the file path for
     * @return A String file path
     */
    public String getPath(RefactoringEventData data) {
        PsiElement element = getPsiElement(data);
        return element != null ? element.getContainingFile().getVirtualFile().getPath() : null;
    }

    /**
     * Get the PsiElement for the RefactoringEventData
     *
     * @param data The data to get the element for
     * @return A PsiElement
     */
    public PsiElement getPsiElement(RefactoringEventData data) {
        return data.getUserData(RefactoringEventData.PSI_ELEMENT_KEY);
    }

    /**
     * Set the data post-refactoring
     *
     * @param afterData The refactoring event data
     */
    public void setAfterData(RefactoringEventData afterData) {
        this.afterData = afterData;
        // update the path too
        afterPath = getPath(afterData);
    }

    /**
     * Set the data pre-refactoring
     *
     * @param beforeData The refactoring event data
     */
    public void setBeforeData(RefactoringEventData beforeData) {
        this.beforeData = beforeData;
        // update the path too
        beforePath = getPath(beforeData);
    }

    /**
     * Set the conflicting data
     *
     * @param conflictsData The refactoring event data
     */
    public void setConflictsData(RefactoringEventData conflictsData) {
        this.conflictsData = conflictsData;
    }

    /**
     * Undo the refactoring action
     *
     * @param tracker The ProjectTracker to remove changes from
     */
    public void undo(ProjectTracker tracker) {
        switch (id) {
            case "refactoring.rename":
                executeRename(tracker, true);
                break;
        }
    }
}
