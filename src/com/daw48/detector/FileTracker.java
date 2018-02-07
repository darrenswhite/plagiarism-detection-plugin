package com.daw48.detector;

import com.intellij.openapi.diagnostic.Logger;

import java.io.Serializable;
import java.util.Base64;
import java.util.LinkedList;
import java.util.List;

/**
 * @author Darren S. White
 */
public class FileTracker implements Serializable {
    /**
     * The Logger for this class
     */
    private static final Logger LOG = Logger.getInstance(FileTracker.class);

    /**
     * The path for this file
     */
    public String path;

    /**
     * The List of Changes for this file
     */
    public List<Change> changes = new LinkedList<>();

    /**
     * The cached file contents
     * <p>
     * Used for checking if a file was changed externally
     */
    public String cache;

    /**
     * Default constructor used for Serialisation
     */
    public FileTracker() {
    }

    /**
     * Create a new FileTracker with the file path
     *
     * @param path The file path for this tracker
     */
    public FileTracker(String path) {
        this.path = path;
    }

    /**
     * Add a new Change for this file
     * <p>
     * Also updates the cached contents
     *
     * @param c The change to track
     */
    public void addChange(Change c, String cache) {
        LOG.info("Adding change: " + c.toString());
        changes.add(c);
        this.cache = Base64.getEncoder().encodeToString(cache.getBytes());
    }
}
