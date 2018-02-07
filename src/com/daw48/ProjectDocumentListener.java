package com.daw48;

import com.intellij.openapi.components.ProjectComponent;
import com.intellij.openapi.editor.EditorFactory;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.editor.event.DocumentListener;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

/**
 * This class listens for changes in a Document per Project
 *
 * @author Darren S. White
 */
public class ProjectDocumentListener implements DocumentListener, ProjectComponent {
    /**
     * The current Project
     */
    private final Project project;

    /**
     * The tracker for all of the Changes
     */
    private final ChangeTracker changeTracker;

    /**
     * Create a new ProjectDocumentListener
     *
     * @param project The current Project
     */
    public ProjectDocumentListener(@NotNull Project project) {
        this.project = project;
        this.changeTracker = ChangeTracker.getInstance(project);
    }

    @Override
    public void documentChanged(DocumentEvent event) {
        changeTracker.processDocumentEvent(event);
    }

    @Override
    public void projectClosed() {
        EditorFactory.getInstance().getEventMulticaster()
                .removeDocumentListener(this);
    }

    @Override
    public void projectOpened() {
        EditorFactory.getInstance().getEventMulticaster()
                .addDocumentListener(this, project);
    }
}
