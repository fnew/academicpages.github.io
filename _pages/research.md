---
layout: archive
title: "Research"
permalink: /research/research.md
author_profile: true
redirect: /research/
---

{% include base_path %}

{% for post in site.research reversed %}
  {% include archive-single.html %}
{% endfor %}
