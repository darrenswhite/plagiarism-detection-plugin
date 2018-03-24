package com.daw48.detector;

import com.daw48.detector.util.CipherUtil;

import java.util.Base64;
import java.util.HashMap;

/**
 * @author Darren S. White
 */
public class CipherTest extends BaseTest {

    private static final HashMap<String, String> ciphered = new HashMap<String, String>() {{
        put("fileA", "Y5aEEoKNUf7gucOFM9Ae3qdCR2fE972c+EAhhK3gNJ5bzxtC2VsCgl0YsT609IHenxzQbLbyGZU0eGJKILA21V15PH+5byIpx411dhrYYDWKVITkgs3OcfjWGvKjY0gYxroMxn1ZJ+fEiHQPJR8iWvFxWxz1cnuCiCyhcoOssVZQQgk57o67RhR0shlJehq1oi1CwPTM7ZR41mFthJeH40ryuSPQLJaibSuKLVkqWpCzl3kJznrQb9AdN35eU57RiIpJZYxxjXRIYR68u3Pnz5BOpVSDzZiOMSzyzHrOi9xVVfpcqJFce90d5uef40za+nlHzzDIfBUwvYQtwOaZD/Scww3OWpRsVRUAuVCdraqQOQk8IqVMNUDkRtN8QOcr+ohVJFJ2gNYv0f4/CXF64DerasnBYbFrJkIv6IaW/SKTF5FVboRmv3phdpV3BFrSMwvhizjkR1S/IUMfrs3OZrOUap+kiaaTa/RY3iCPlC4v67qj3NXOjFsS/li0u3pm");
    }};
    private static final HashMap<String, FileTracker> original = new HashMap<String, FileTracker>() {{
        FileTracker fileA = new FileTracker();
        fileA.cache = Base64.getEncoder().encodeToString("fileA_contents".getBytes());
        fileA.changes.add(new Change(0, "", "fileA_contents",
                Change.Source.OTHER, 10));
        fileA.path = "fileA";
        put("fileA", fileA);
    }};

    public void testCipher() {
        assertEquals(CipherUtil.cipher(original), ciphered);
    }

    public void testDecipher() {
        assertEquals(CipherUtil.decipher(ciphered, FileTracker.class), original);
    }
}
