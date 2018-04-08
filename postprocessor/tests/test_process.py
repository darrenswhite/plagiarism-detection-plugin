from io import StringIO

from tests.base import BaseTest

# Encrypted submission data to process
SUBMISSION_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="PlagiarismDetectorProjectComponent">
    <option name="files">
      <map>
        <entry key="src/A.java" value="Y5aEEoKNUf7gucOFM9Ae3qdCR2fE972c+EAhhK3gNJ5EqjARwLucmo11pqh+GOukwShtE2/jZLx+hu//yo8L1W1vMFX1xbzdP1cyl7xng6oUCW/hntC36zugzUbQQ/KFb2HoMJtQTfkUSCQWh7wiZMef+7a83FN7zp64vHK3S7HLdmfEtJLxNsiIGhXv/bS3EVkz4tU2G8Td5to991r5hm+ZFi1ksbaX2nfxg2IxtY7CYfp8gVPjAwe0xQSkp/v8VJNKnzaGXQjM/348ltSsGUlClNrXdlU1EBlsE+tToWyrRe0a93L6SeCYCtm/dtIMXebK287aZmPp0eFgkeYv7vWOIu2DsryJK33hnTDrcOp79Hq3/dR7FPUFg0zNcWvP97HEXVDFoM7Xhyi1EnxOpZybwzGXuiUe+NZTivY6RZna66t8c4jmpOOE+0GuQR30UxFiYFQDZ4sKkRcHj5Ijqvp5R88wyHwVML2ELcDmmQ/PE4Yp1Y6Q29PQmf1cjaTYTsSxVGIMAchacLTlicL54xqya8I7F1GysClarpv4j2th9AZn6/Gsicjd92N9HuI1SxkWOrVcBpVjLdQ68yS1wR0u50cjWCOUkgz2g7beKqgLEI0voRDPY+Y8CMakWYlclDMQ+0asDhiDReSktTrFDmWxyn8HCXmqLRAibr6HXMYMfQdmb498KP0gTAyzZaMeqez8BW44nAbBODTWdJcyCJaCTpA7UGQMg7J26IqaBZoXbniTXFiGE0c9IClQf32iXVSF9U4JCSxBIEd5+5D6Pc3resxkPtho21qvEpVUwXH+qzEAbC8WnIeIf7B8pHm2Mto/LDRuSSwAoko64WIdTw==" />
        <entry key="src/B.java" value="Y5aEEoKNUf7gucOFM9Ae3qdCR2fE972c+EAhhK3gNJ76gjpz6UEa3WtAMtxVO6scwShtE2/jZLx+hu//yo8L1W1vMFX1xbzdP1cyl7xng6oUCW/hntC36zugzUbQQ/KFb2HoMJtQTfkUSCQWh7wiZMef+7a83FN7zp64vHK3S7HLdmfEtJLxNsiIGhXv/bS3UHg5U+/T9WVpasuMkhtz+oYxWIbB/8BiVNDlGFWpe95NjZ9iuXHsd5Uj/ZRKqeOjOlPDII8Lp5zPMC/do8syPuqhKk4wGM/2+vx9xuupPzLoRz43C50BCX/AlX/HvePUzfQGPJ1wwyB08I3tjW3hpf/oCA66iB3NPWl+HUfmFFFiprsMTyiAw8yrsVOcv6jnT+7h2yt323rSP1GFmhXa3MR4CmFmoddiSET2WVKaaq4bs48ToC1toSha7Kj1UZRC3D3BaPx4AVVWBd7JkL5gkbUSd7KjxTtvVTrRaOxJwWhVKOYK7Y1hNlX+mBwrnVyu5vW+yTsRK9l/WHmyPuxK2FXuy0Qoi8oYDWvKRvH4CjpUfKOJ5aQahM19cWR4ZSS3ys8eFAaiEq8mPpFdVxtdQxqya8I7F1GysClarpv4j2th9AZn6/Gsicjd92N9HuI1SxkWOrVcBpVjLdQ68yS1wR0u50cjWCOUkgz2g7beKqgLEI0voRDPY+Y8CMakWYlclDMQ+0asDhiDReSktTrFDmWxyn8HCXmqLRAibr6HXMYnH+SBclvylkmsTFBIIszn75fV6IUH1HaP3U8z843wUeYOTndOeXvK+0TyoTDtigEdt4+wNf1ts1PQd//bUk+58AdWV7TPhf5ljHmznZe5KAu8ss8CZaMFDhAfILavolXnfm/SPFjMkn+so5gu9HMCuawcou+NbJB6Dgha4h6MqPA1ZsWF2Lmh0nOJIjCswKQasmvCOxdRsrApWq6b+I9rIZVdW3Iq80k6DiGcWOTvpcZO04FfaVxNzj8swvsZNndjlkDlruzwlurdZV5aUbLU+W/ienPklDFqcWDs9OFvAbxRpY1wqpz8Wdffn3ZBI5zMMMoe00TaBk5EHL6Xy77F8rTj9vqW6Pf7UN2lBG/5xAYOXEgSCEGJr6lFmDeXQfga/Y9kNKtrvzDXFjmEGcZN8bBdO94/V9Ol6zerO3EPvlxt3SEJBUCvhlqJfkgsdKE=" />
        <entry key="src/C.java" value="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" />
        <entry key="src/Test.java" value="Y5aEEoKNUf7gucOFM9Ae3qdCR2fE972c+EAhhK3gNJ4JTLe2YEs9h2ZtIEAMRx0I7HrifXtlOK+IFfcbgw27CyXvUcQL4b4lKUGm+0IxSLI/L3Jw6qWVgbCeJiEscgMo5g5Od055e8r7RPKhMO2KAR23j7A1/W2zU9B3/9tST7nwB1ZXtM+F/mWMebOdl7koC7yyzwJlowUOEB8gtq+iVfp5R88wyHwVML2ELcDmmQ/xD8TNEhBfoLQ9ovHNii1kNQV8ZfArvMDQFNW5ubH5IgqcfNwzIsnfnWtVDHpuqwFRHiZ2BS+g88005a/cw1E7QzFuX511dCVvznk7W3zX2dAQjhn6+RJUwomXn0k6U7Lmccucs3x2CZUcsWskH/owqLW++C1ryV5cRPv3VPxZsKPBhuZDcvh62//FxJe4Wd+T8xvg79fdOg37Sv/i2uBsDTwQFnMms5q2cqsYEC9yqWt+wTURVs01qypPVglQBfZTxn3xz/JikawSv441Cgr+ZmGnP185B7p+w5M6qUyRjUSyUhL+HelJwUcQIzJQ9tcaqB9nVrtG1glL7f3nPYeUtEoQI/yXcNdzDjMYOc7VUBshgMDCI5jrusG3HgYpQkiEut51//lbx3AwkeiRH7CWoi1CwPTM7ZR41mFthJeH48oXNac6SixfDmTDk3SPYEh7DnHw/ZJN3FV5bTMaxy3rGrJrwjsXUbKwKVqum/iPa10sRTikVa+7Hzl1I7RMrLwqjKOj8rBpfy9wAw6s1Dnlf3KL1LJlrxLKwqMOju8InxARUF4TrpTU5pQ9zB8sFjY598b+ra3EcNdRkoMZy55/+ZanhCphEScxwcpmnYXLNZWMIrJSO7EP4w8fEX+pweCyjvhp23I940jRLkqNFNkV+nlHzzDIfBUwvYQtwOaZD/EPxM0SEF+gtD2i8c2KLWRoZ7d0bzT/hgRD9UBTLY+0Io9V6PQuqEE86vj/8ToUReFxX/GfI5W0YNQvRGgR4IWUznbFTRsswau9h0xPOK6QwICNOJK7yeezYR1OC2oK4U4NVgcv4eBYYzV21uFYIowzjLta3O/ZvLXX1Me+qVwgprzpYiVHiDEMC5NkroaInEUnZ9qQp4ETj5e7tBVOVcTTMYALTws14KgDZbfjetAy3BsOJsLo5/Lm0QsCNUes2hZZAk5XigCyp6GLaXZ9GSskuxxU40fCpefqUSEzUJmr" />
      </map>
    </option>
  </component>
</project>"""

# Expected submission result from post processing
SUBMISSION_RESULT = {
    'src/A.java': {
        'diff_ratio': 0.0,
        'frequency_total': -23,
        'frequency_clipboard': 0,
        'frequency_external': 0,
        'frequency_other': -23,
        'frequency_time_source_data': [
            {'f': -21, 's': 'OTHER', 't': 1522108577165},
            {'f': -2, 's': 'OTHER', 't': 1522108577279}
        ]
    },
    'src/B.java': {
        'diff_ratio': 1.0,
        'frequency_total': 19,
        'frequency_clipboard': 0,
        'frequency_external': 0,
        'frequency_other': 19,
        'frequency_time_source_data': [
            {'f': 42, 's': 'OTHER', 't': 1522108657566},
            {'f': -21, 's': 'OTHER', 't': 1522108657662},
            {'f': -2, 's': 'OTHER', 't': 1522108657694}
        ],
    },
    'src/C.java': {
        'diff_ratio': 0.9464285714285714,
        'frequency_total': 56,
        'frequency_clipboard': 0,
        'frequency_external': 56,
        'frequency_other': 0,
        'frequency_time_source_data': [
            {'f': 5, 's': 'OTHER', 't': 1522108919242},
            {'f': 56, 's': 'EXTERNAL', 't': 1522108919243},
            {'f': 0, 's': 'OTHER', 't': 1522108919278},
            {'f': 5, 's': 'OTHER', 't': 1522108938281},
            {'f': 0, 's': 'OTHER', 't': 1522108938327},
            {'f': -4, 's': 'OTHER', 't': 1522108939012},
            {'f': 4, 's': 'OTHER', 't': 1522108947829},
            {'f': -5, 's': 'OTHER', 't': 1522108947843},
            {'f': -5, 's': 'OTHER', 't': 1522108948240}
        ]
    },
    'src/Test.java': {
        'diff_ratio': 1.0,
        'frequency_total': 22,
        'frequency_clipboard': 0,
        'frequency_external': 0,
        'frequency_other': 22,
        'frequency_time_source_data': [
            {'f': 45, 's': 'OTHER', 't': 1522108498856},
            {'f': -21, 's': 'OTHER', 't': 1522108499016},
            {'f': -2, 's': 'OTHER', 't': 1522108499093}
        ]
    }
}


class TestProcess(BaseTest):
    def test_process(self):
        # Post process the submission
        result = self.pp.run(StringIO(SUBMISSION_DATA))
        # Check the result
        self.assertEqual(result, SUBMISSION_RESULT)
