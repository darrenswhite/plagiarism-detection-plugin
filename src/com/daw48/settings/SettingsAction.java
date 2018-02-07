package com.daw48.settings;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.ui.Messages;

/**
 * An Action to change the Settings
 *
 * @author Darren S. White
 */
public class SettingsAction extends AnAction {

    private static final String MESSAGE = "Hello, %s!\nI am glad to see you.";
    private static final String TITLE = "Information";

    @Override
    public void actionPerformed(AnActionEvent event) {
        final Settings settings = Settings.getInstance();

        while (settings.name == null) {
            settings.name = Messages.showInputDialog(
                    "What is your name?", "Input Your Name",
                    Messages.getQuestionIcon());
        }

        Messages.showMessageDialog(String.format(MESSAGE, settings.name),
                TITLE, Messages.getInformationIcon());
    }
}
