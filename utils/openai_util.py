#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# You: 你喜欢我么?\nFriend: 喜欢.\nYou: 你喜欢我什么?\nFriend:

def davin_ci_002(prompt):
    return dict(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=3000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
