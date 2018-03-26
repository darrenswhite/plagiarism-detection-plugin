package com.daw48.detector.util;

import com.daw48.detector.FileTracker;
import com.daw48.detector.ProjectTracker;
import com.intellij.psi.PsiClass;
import com.intellij.psi.PsiElement;
import com.intellij.refactoring.listeners.RefactoringEventData;

public class RefactoringData {

    private final String id;
    private RefactoringEventData beforeData;
    private RefactoringEventData afterData;
    private RefactoringEventData conflictsData;
    private String beforePath;
    private String afterPath;

    public RefactoringData(String id) {
        this.id = id;

    }

    public void execute(ProjectTracker tracker) {
        switch (id) {
            case "refactoring.rename":
                executeRename(tracker, false);
                break;
        }
    }

    private void executeRename(ProjectTracker tracker, boolean undo) {
        // Only file/class renaming is currently supported
        if (getPsiElement(beforeData) instanceof PsiClass) {
            String beforePath = undo ? this.afterPath : this.beforePath;
            String afterPath = undo ? this.beforePath : this.afterPath;
            if (tracker.files.containsKey(beforePath)) {
                FileTracker ft = tracker.files.remove(beforePath);
                ft.path = afterPath;
                tracker.files.put(afterPath, ft);
            }
        }
    }

    public String getPath(RefactoringEventData data) {
        PsiElement element = getPsiElement(data);
        return element != null ? element.getContainingFile().getVirtualFile().getPath() : null;
    }

    public PsiElement getPsiElement(RefactoringEventData data) {
        return data.getUserData(RefactoringEventData.PSI_ELEMENT_KEY);
    }

    public void setAfterData(RefactoringEventData afterData) {
        this.afterData = afterData;
        afterPath = getPath(afterData);
    }

    public void setBeforeData(RefactoringEventData beforeData) {
        this.beforeData = beforeData;
        beforePath = getPath(beforeData);
    }

    public void setConflictsData(RefactoringEventData conflictsData) {
        this.conflictsData = conflictsData;
    }

    public void undo(ProjectTracker tracker) {
        switch (id) {
            case "refactoring.rename":
                executeRename(tracker, true);
                break;
        }
    }
}
