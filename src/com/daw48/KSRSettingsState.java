package com.daw48;

import com.intellij.openapi.components.*;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@State(name = "KSRSettingsState", storages = @Storage(StoragePathMacros.WORKSPACE_FILE))
public class KSRSettingsState implements PersistentStateComponent<KSRSettingsState.State> {
    private State state = new State();

    @Override
    public State getState() {
        return state;
    }

    public static KSRSettingsState getInstance(@NotNull Project project) {
        return ServiceManager.getService(project, KSRSettingsState.class);
    }

    @Nullable
    public String getName() {
        return state.name;
    }

    public void setName(@NotNull String name) {
        state.name = name;
    }

    @Override
    public void loadState(@NotNull State state) {
        this.state = state;
    }

    public static class State {
        @Nullable
        public String name = null;
    }
}
