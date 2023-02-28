<script>
    import '@picocss/pico';
</script>

<header class='container-fluid'>
    <nav>
        <ul>
            <li><a href='/' role="button" class="outline" rel='external'>
                <!-- <Icon src="{Home}" theme="mini" size="10%"/> -->
                Home
            </a></li>
        </ul>
        <ul>
            <li><strong>OTCIC Dashboard</strong></li>
        </ul>
        <ul>
            <li><a href='/' role="button" class="outline">
                <!-- <Icon src="{ArrowsRightLeft}" theme="mini" size="5%"/> Switch View -->
                Switch view
            </a></li>
        </ul>
    </nav>
</header>

<main class='container'>
    <slot />
</main>