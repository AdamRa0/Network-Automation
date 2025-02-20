def provide_filter_string(query: str) -> str:
    """
    Arguments
    ---------
    query: namespace to filter from running config

    Returns
    ---------
    Config filter string
    """
    return f"""
    <filter type="xpath">{query}</filter>
    """

    # /ipi-interface:interfaces/ipi-interface:interface