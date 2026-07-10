from toontown.battle import SuitBattleGlobals
"""
Cog HP formula.

Terminology:
  - baseLevel: a cog's natural/starting level, 0 through 7 (SuitAttributes['level']).
    Cogs from different tracks that share the same baseLevel (e.g. 'f', 'cc',
    'sc', 'bf', all baseLevel 0) are treated as equivalent and get identical HP.
  - spawnLevel: the actual in-game level a cog spawns at (e.g. 1 through 12).
    This is what player-facing code passes into calculate_hp.

Core idea:
  - Each spawnLevel has a "base" HP given by base_hp(spawnLevel).
  - Each baseLevel can add a bonus on top of that base HP.
  - A spawnLevel's bonus is 0 at the *first* baseLevel it appears in (that's
    the spawnLevel's "first instance" and is left untouched), then grows as
    you move into higher baseLevels.
  - The bonus per baseLevel step isn't fixed -- stepping into a higher
    baseLevel adds more than stepping into a lower one (see
    base_level_step_increment), scaled by that baseLevel's natural (low)
    spawnLevel.
  - Because different spawnLevels start counting their bonus from different
    baseLevels, it's mathematically possible for the raw formula to give a
    *lower* HP to a higher spawnLevel within the same baseLevel. We never
    want that, so the table is "floored": if a cell would be lower than the
    cell directly above it (same baseLevel, one spawnLevel down), it's
    bumped up instead.

    *Note* This formula and its implementation were developed collaboratively 
    with Claude (Anthropic), based on Tardistom's design requirements (tier-based 
    HP scaling, identical HP for cogs sharing a natural level).
"""

# ---------------------------------------------------------------------------
# Tunable game data
# ---------------------------------------------------------------------------

# Which spawnLevels each cog covers, keyed by cog code (e.g. 'f', 'cc', 'sc').
# This is the single source of truth -- the spawnLevel range and baseLevel
# count are both derived from it below.
SUIT_RANGES = SuitBattleGlobals.createLevelRangeDict()

# How much bigger each successive baseLevel's step is (see base_level_step_increment).
BASE_LEVEL_STEP_SCALE = 2

# Levels at/above this get an extra late-game HP bonus (see base_hp).
HIGH_LEVEL_THRESHOLD = 12
HIGH_LEVEL_BONUS_PER_LEVEL = 1.5


# ---------------------------------------------------------------------------
# Derived constants
# ---------------------------------------------------------------------------

NUM_BASE_LEVELS = len(SUIT_RANGES)
MAX_SPAWN_LEVEL = max(high for low, high in SUIT_RANGES.values())


# ---------------------------------------------------------------------------
# Core formulas
# ---------------------------------------------------------------------------

def base_hp(spawnLevel):
    """The HP a spawnLevel would have with no baseLevel bonus at all."""
    hp = (spawnLevel + 1) * (spawnLevel + 2)
    if spawnLevel >= HIGH_LEVEL_THRESHOLD:
        hp += spawnLevel * HIGH_LEVEL_BONUS_PER_LEVEL
    return hp


def get_base_level(cog):
    """A cog's baseLevel is its natural (starting) level -- 0 through 7.
    Cogs sharing the same 'level' in SuitAttributes share the same
    baseLevel, regardless of which track they belong to."""
    return SuitBattleGlobals.SuitAttributes[cog]['level']


def first_base_level_for_spawn_level(spawnLevel):
    """The lowest baseLevel that this spawnLevel appears in, across all cogs."""
    baseLevelsCovering = [
        get_base_level(cog)
        for cog, (low, high) in SUIT_RANGES.items()
        if low <= spawnLevel <= high
    ]
    return min(baseLevelsCovering) if baseLevelsCovering else None


def base_level_step_increment(cog):
    """HP gained by stepping INTO this cog's baseLevel, based on that
    baseLevel's natural (low) spawnLevel. Bigger baseLevels add more."""
    low, high = SUIT_RANGES[cog]
    return BASE_LEVEL_STEP_SCALE * low


def sigma(n):
    """Sum of 1 + 2 + ... + n (the triangular number), computed directly
    instead of looping. Named sigma (Σ) since that's exactly what it is:
    a running total of consecutive integers."""
    return n * (n + 1) / 2


def base_level_bonus(firstBaseLevel, baseLevel):
    """
    Total HP bonus for being at `baseLevel`, for a spawnLevel whose first
    baseLevel was `firstBaseLevel`. This is just the sum of
    base_level_step_increment(b) for every baseLevel b between
    firstBaseLevel+1 and baseLevel, added up via the triangular-number
    shortcut instead of a loop.
    """
    return BASE_LEVEL_STEP_SCALE * (sigma(baseLevel) - sigma(firstBaseLevel))


# ---------------------------------------------------------------------------
# Table construction
# ---------------------------------------------------------------------------

def compute_raw_hp(spawnLevel, cog):
    """HP for (spawnLevel, cog) using the formula alone, ignoring the floor."""
    firstBaseLevel = first_base_level_for_spawn_level(spawnLevel)
    baseLevel = get_base_level(cog)
    return base_hp(spawnLevel) + base_level_bonus(firstBaseLevel, baseLevel)


def build_hp_table():
    """
    Compute HP for every valid (spawnLevel, cog) pair, cog by cog, flooring
    each value at the previous spawnLevel's HP + this cog's baseLevel step
    so HP never decreases as spawnLevel increases within a cog's range.
    """
    table = {}
    for cog, (low, high) in SUIT_RANGES.items():
        previousValue = None
        for spawnLevel in range(low, high + 1):
            value = compute_raw_hp(spawnLevel, cog)
            if previousValue is not None and value <= previousValue:
                value = previousValue + base_level_step_increment(cog)
            value = int(round(value))
            table[(spawnLevel, cog)] = value
            previousValue = value
    return table


HP_TABLE = build_hp_table()


def calculate_hp(spawnLevel, cog):
    """Return the cog HP for a given spawnLevel and cog code (e.g. 'f', 'cc')."""
    return HP_TABLE[(spawnLevel, cog)]