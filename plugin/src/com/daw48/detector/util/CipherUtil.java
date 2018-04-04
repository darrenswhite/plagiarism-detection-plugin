package com.daw48.detector.util;

import com.intellij.openapi.diagnostic.Logger;
import com.intellij.util.xmlb.XmlSerializer;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;
import org.jdom.output.XMLOutputter;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * This class is used to encrypt/decrypt Map data structures
 *
 * @author Darren S. White
 */
public class CipherUtil {
    /**
     * The Logger for this class
     */
    private static final Logger LOG = Logger.getInstance(CipherUtil.class);

    /**
     * Cipher key used for encryption & decryption
     */
    private static final Key key = new SecretKeySpec("plagiarismplugin".getBytes(), "AES");

    /**
     * Encrypts this Map using AES encryption
     * <p>
     * This will first serialise each value into an XML String representation.
     * Each of the XML values are then encrypted and then Base64 encoding
     * is applied.
     *
     * @param map The Map to be encrypted
     * @return The AES encrypted Map
     */
    public static Map<String, String> cipher(Map<String, ?> map) {
        Map<String, String> cipheredMap = new HashMap<>();
        try {
            // Use AES to encrypt
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            // Encrypt each entry individually
            for (Map.Entry<String, ?> entry : map.entrySet()) {
                try {
                    // Convert the value to XML format first
                    String xml = serialize(entry.getValue());
                    // Encrypt the XML string and apply base64 encoding
                    String ciphered = Base64.getEncoder().encodeToString(cipher.doFinal(xml.getBytes()));
                    cipheredMap.put(entry.getKey(), ciphered);
                } catch (BadPaddingException | IllegalBlockSizeException e) {
                    LOG.error("Error ciphering object: ", e);
                }
            }
        } catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException e) {
            LOG.error("Error initializing cipher: ", e);
        }
        return cipheredMap;
    }

    /**
     * Decrypts the given map using AES
     *
     * @param cipherMap The encrypted Map to decrypt
     * @param clazz     The class for the Map value to expect
     * @param <V>       The generic type for the Map value
     * @return The decrypted Map
     */
    public static <V> Map<String, V> decipher(Map<String, String> cipherMap, Class<V> clazz) {
        Map<String, V> decipheredMap = new HashMap<>();
        try {
            // Use AES to decrypt
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.DECRYPT_MODE, key);
            // Decrypt each entry individually
            for (Map.Entry<String, String> entry : cipherMap.entrySet()) {
                try {
                    // Decrypt the base64 decoded value first
                    byte[] deciphered = cipher.doFinal(Base64.getDecoder().decode(entry.getValue()));
                    // Finally deserialize the data
                    decipheredMap.put(entry.getKey(), deserialize(deciphered, clazz));
                } catch (BadPaddingException | IllegalBlockSizeException | JDOMException | IOException e) {
                    LOG.error("Error deciphering object: ", e);
                }
            }
        } catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException e) {
            LOG.error("Error initializing cipher: ", e);
        }
        return decipheredMap;
    }

    /**
     * Deserialize XML byte[] data into an Object of type V
     *
     * @param data  The XML data in byte[] form to deserialize
     * @param clazz The class of the value being deserialized
     * @param <V>   The type of value being deserialized
     * @return The XML byte[] deserialized object
     * @throws JDOMException If a JDOMException occurs
     * @throws IOException   If an IOException occurs
     */
    private static <V> V deserialize(byte[] data, Class<V> clazz) throws JDOMException, IOException {
        Document document = new SAXBuilder().build(new ByteArrayInputStream(data));
        Element element = document.getRootElement();
        return XmlSerializer.deserialize(element, clazz);
    }

    /**
     * Serialize an Object into an XML String
     *
     * @param object The object to serialize into XML format. Must be
     *               Serializable
     * @return The XML String value of the Object
     */
    private static String serialize(Object object) {
        Element element = XmlSerializer.serialize(object);
        return new XMLOutputter().outputString(element);
    }
}
