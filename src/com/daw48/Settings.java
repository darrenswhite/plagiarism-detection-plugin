package com.daw48;

import com.intellij.openapi.components.*;
import com.intellij.openapi.project.Project;
import com.intellij.util.xmlb.XmlSerializerUtil;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@State(name = "KSR", storages = @Storage(StoragePathMacros.WORKSPACE_FILE))
public class Settings implements PersistentStateComponent<Settings> {
    public String name = null;

    @Nullable
    @Override
    public Settings getState() {
        return this;
    }

    public static Settings getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, Settings.class);
    }

    @Override
    public void loadState(@NotNull Settings state) {
        XmlSerializerUtil.copyBean(state, this);
    }
}
