"""Entry point for the story creation application."""

import asyncio

import config, kernel_factory, plugins, agents, loop, seed_loader

def main():
    """Initialize and run the story creation process."""
    # Load configuration
    cfg = config.Config.from_env()
    
    # Initialize kernel and plugins
    kernel = kernel_factory.build_kernel(cfg)

    from plugins import writer_plugin, editor_plugin, selector_plugin, illustrator_plugin
    
    pl_writer = writer_plugin.build_writer_plugin()
    pl_editor = editor_plugin.build_editor_plugin()
    pl_selector = selector_plugin.build_selector_plugin()
    pl_illustrator = illustrator_plugin.build_illustrator_plugin()
    
    for p in (pl_writer, pl_editor, pl_selector, pl_illustrator):
        kernel.plugins[p.name] = p

    # Create agents
    agent_writer = agents.WriterAgent(kernel)
    agent_editor = agents.EditorAgent(kernel)
    agent_selector = agents.SelectorAgent(kernel)
    agent_illustrator = agents.IllustratorAgent(kernel)

    # Load seed and create run loop
    seed = seed_loader.load_seed()
    run_loop = loop.RunLoop(
        writer=agent_writer,
        editor=agent_editor,
        selector=agent_selector,
        illustrator=agent_illustrator,
        seed=seed,
        max_turns=cfg.max_turns
    )

    # Run it
    asyncio.run(run_loop.run())

if __name__ == "__main__":
    main()
