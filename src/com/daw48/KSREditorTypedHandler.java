package com.daw48;

import com.intellij.codeInsight.editorActions.TypedHandlerDelegate;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;

public class KSREditorTypedHandler extends TypedHandlerDelegate {

    @Override
    public Result checkAutoPopup(char charTyped, Project project, Editor editor, PsiFile file) {
        System.out.println(charTyped);
        return Result.CONTINUE;
    }

    @Override
    public Result beforeSelectionRemoved(char c, Project project, Editor editor, PsiFile file) {
        System.out.println(c);
        return Result.CONTINUE;
    }

    @Override
    public Result beforeCharTyped(char c, Project project, Editor editor, PsiFile file, FileType fileType) {
        System.out.println(c);
        return Result.CONTINUE;
    }

    @Override
    public Result charTyped(char c, Project project, @NotNull Editor editor, @NotNull PsiFile file) {
        System.out.println(c);
        return Result.CONTINUE;
    }
}
