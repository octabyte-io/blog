---
draft: false
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
date: {{ .Date }}
description: "DESCRIPTION_GOES_HERE"
tags: [KEYWORDS_GOES_HERE]
categories: ["Fully managed", CATEGORIES]
cover:
  image: images/cover.png
  caption: '{{ replace .File.ContentBaseName "-" " " | title }}'
  relative: true
ShowToc: true
TocOpen: true
---