package com.daw48.detector;

import org.jetbrains.annotations.NotNull;

import java.io.Serializable;
import java.util.Objects;

/**
 * A class that describes a Document Change
 *
 * @author Darren S. White
 */
public class Change implements Serializable {
    /**
     * The index where the changes start
     */
    public int offset;

    /**
     * The old String that was removed or replaced
     */
    public String oldString;

    /**
     * The new String that was inserted
     */
    public String newString;

    /**
     * The type of change
     */
    public Source source;

    /**
     * The timestamp of the Change
     */
    public long timestamp;

    /**
     * Default constructor used for Serialisation
     */
    public Change() {
    }

    /**
     * Create a new Change
     *
     * @param offset    The index where the changes start
     * @param oldString The old String that was removed or replaced
     * @param newString The new String that was inserted
     * @param source    The type of change
     * @param timestamp The timestamp of the Change
     */
    public Change(int offset, @NotNull String oldString,
                  @NotNull String newString, @NotNull Source source,
                  long timestamp) {
        this.offset = offset;
        this.oldString = oldString;
        this.newString = newString;
        this.source = source;
        this.timestamp = timestamp;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        } else if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Change change = (Change) o;
        return offset == change.offset &&
                timestamp == change.timestamp &&
                Objects.equals(oldString, change.oldString) &&
                Objects.equals(newString, change.newString) &&
                source == change.source;
    }

    @Override
    public int hashCode() {
        return Objects.hash(offset, oldString, newString, source, timestamp);
    }

    @Override
    public String toString() {
        return "Change{" +
                "offset=" + offset +
                ", oldString=" + oldString +
                ", newString=" + newString +
                ", source=" + source +
                ", timestamp=" + timestamp +
                '}';
    }

    /**
     * The origin of the Change
     *
     * @author Darren S. White
     */
    public enum Source {
        CLIPBOARD,
        CODE_GENERATION,
        EXTERNAL,
        OTHER,
    }
}
