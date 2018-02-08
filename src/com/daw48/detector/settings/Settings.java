package com.daw48.detector.settings;

import com.intellij.openapi.components.PersistentStateComponent;
import com.intellij.openapi.components.ServiceManager;
import com.intellij.openapi.components.State;
import com.intellij.openapi.components.Storage;
import com.intellij.util.xmlb.XmlSerializerUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Settings class. The settings are stored in an xml file for persistence.
 *
 * @author Darren S. White
 */
@State(name = "PlagiarismDetectionSettingsComponent",
        storages = @Storage("plagiarism_detection_settings.xml"))
public class Settings implements PersistentStateComponent<Settings> {
    public String name;

    /**
     * Gets the current instance for this class
     *
     * @return A Settings instance
     */
    public static Settings getInstance() {
        return ServiceManager.getService(Settings.class);
    }

    @Nullable
    @Override
    public Settings getState() {
        return this;
    }

    @Override
    public void loadState(@NotNull Settings state) {
        XmlSerializerUtil.copyBean(state, this);
    }
}
