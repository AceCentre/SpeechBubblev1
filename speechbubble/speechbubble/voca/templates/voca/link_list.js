var tinyMCELinkList = new Array(
    ["##DEVICES##", ""],
{% for device in devices %}
    ["{{ device.name }}", "/device/{{ device.slug }}"],
{% endfor %}
    ["##SOFTWARE##", ""],
{% for software in softwares %}
    ["{{ software.name }}", "/software/{{ software.slug }}"],
{% endfor %}
    ["##VOCABULARIES##", ""],
{% for vocabulary in vocabularies %}
    ["{{ vocabulary.name }}", "/vocabulary/{{ vocabulary.slug }}"],
{% endfor %}
    ["Home Page", "/"]
);
