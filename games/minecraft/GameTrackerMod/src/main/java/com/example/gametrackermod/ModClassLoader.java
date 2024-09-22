package com.example.gametrackermod;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.logging.Logger;

public class ModClassLoader {
    private static final Logger LOGGER = Logger.getLogger(ModClassLoader.class.getName());

    public static void loadExternalLibraries() throws IOException {
        // Log the location of the libraries folder
        File librariesDir = new File(ModClassLoader.class.getResource("/META-INF/libraries").getFile());
        LOGGER.info("Looking for libraries in: " + librariesDir.getAbsolutePath());

        if (librariesDir.exists() && librariesDir.isDirectory()) {
            File[] jarFiles = librariesDir.listFiles((dir, name) -> name.endsWith(".jar"));
            if (jarFiles != null) {
                for (File jar : jarFiles) {
                    LOGGER.info("Found library: " + jar.getName());
                    URLClassLoader classLoader = (URLClassLoader) ClassLoader.getSystemClassLoader();
                    URL jarURL = jar.toURI().toURL();
                    addURLToClassLoader(classLoader, jarURL);
                    LOGGER.info("Added to classpath: " + jarURL);
                }
            } else {
                LOGGER.warning("No JAR files found in the libraries directory.");
            }
        } else {
            LOGGER.warning("Libraries directory not found or not a directory.");
        }
    }

    private static void addURLToClassLoader(URLClassLoader classLoader, URL url) throws IOException {
        try {
            var method = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
            method.setAccessible(true);
            method.invoke(classLoader, url);
        } catch (ReflectiveOperationException e) {
            throw new IOException("Failed to add URL to system classloader", e);
        }
    }
}