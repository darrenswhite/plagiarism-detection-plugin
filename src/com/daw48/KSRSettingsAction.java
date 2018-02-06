package com.daw48;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.PlatformDataKeys;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;

public class KSRSettingsAction extends AnAction {

    @Override
    public void actionPerformed(AnActionEvent event) {
        final Project project = event.getData(PlatformDataKeys.PROJECT);
        assert (project != null);

        final KSRSettingsState service = KSRSettingsState.getInstance(project);
        String name = service.getName();

        while (name == null) {
            name = Messages.showInputDialog(project, "What is your name?", "Input Your Name", Messages.getQuestionIcon());
        }

        service.setName(name);

        Messages.showMessageDialog(project, "Hello, " + name + "!\n I am glad to see you.", "Information", Messages.getInformationIcon());
    }
}
