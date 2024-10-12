def EscapeMarkdown(string_Input):
    string_Input = string_Input.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace(
        "(", "\\(").replace(")", "\\)").replace("~", "\\~").replace(">", "\\>").replace("#", "\\#").replace("+",
                                                                                                            "\\+").replace(
        "-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".",
                                                                                                            "\\.").replace(
        "!", "\\!")
    return string_Input
