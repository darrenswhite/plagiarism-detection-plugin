package com.daw48.detector;

import com.daw48.detector.util.DocumentUtil;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.components.ProjectComponent;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.EditorFactory;
import com.intellij.openapi.editor.event.DocumentEvent;
import com.intellij.openapi.editor.event.DocumentListener;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import org.apache.commons.compress.utils.IOUtils;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.util.*;

/**
 * This class listens for changes in a Document per Project
 *
 * @author Darren S. White
 */
public class ProjectDocumentListener implements DocumentListener,
        ProjectComponent {
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
     * Create a new ProjectDocumentListener
     *
     * @param project The current Project
     */
    public ProjectDocumentListener(@NotNull Project project) {
        this.project = project;
        this.tracker = ProjectTracker.getInstance(project);
    }

    /**
     * Checks if any of the tracked files were changed externally
     * <p>
     * This works by comparing the base64 encoded cache for each file against
     * its current base64 encoded content
     */
    private void checkCachedExternalChanges() {
        for (Map.Entry<String, FileTracker> entry : tracker.files.entrySet()) {
            String path = entry.getKey();
            FileTracker tracker = entry.getValue();
            VirtualFile file = LocalFileSystem.getInstance()
                    .findFileByPath(path);

            if (file == null) {
                continue;
            }

            try {
                String cachedContent = new String(Base64.getDecoder()
                        .decode(entry.getValue().cache));

                file.refresh(false, false);

                if (file.exists()) {
                    String newContent = new String(IOUtils.toByteArray(
                            file.getInputStream()));

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
        if (!file.getPath().contains(".idea/")) {
            // Track the change
            tracker.processDocumentEvent(event);
        }
    }

    private List<Change> getChanges(String cachedContent, String newContent) {
        List<Change> changes = new ArrayList<>();
        // TODO Write algorithm to find changes between cached and new content
        return changes;
    }

    @Override
    public void projectClosed() {
        EditorFactory.getInstance().getEventMulticaster()
                .removeDocumentListener(this);
    }

    @Override
    public void projectOpened() {
        ApplicationManager.getApplication().runReadAction(() -> {
            checkCachedExternalChanges();
            EditorFactory.getInstance().getEventMulticaster()
                    .addDocumentListener(this, project);
        });
    }
}
