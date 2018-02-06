package com.daw48.settings;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.PlatformDataKeys;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;

public class SettingsAction extends AnAction {

    private static final String MESSAGE = "Hello, %s!\nI am glad to see you.";
    private static final String TITLE = "Information";

    @Override
    public void actionPerformed(AnActionEvent event) {
        final Project project = event.getData(PlatformDataKeys.PROJECT);
        assert (project != null);

        final Settings settings = Settings.getInstance(project);

        while (settings.name == null) {
            settings.name = Messages.showInputDialog(project,
                    "What is your name?",
                    "Input Your Name",
                    Messages.getQuestionIcon());
        }

        Messages.showMessageDialog(project,
                String.format(MESSAGE, settings.name),
                TITLE,
                Messages.getInformationIcon());
    }
}
