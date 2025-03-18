from items import *
from .spawn_params import ItemSpawnParams

#Spawn lists!
ItemSpawns = []                                                         

# Can specify min_floor, max_floor, branch allowed - by default can spawn anywhere
# Weapons
ItemSpawns.append(ItemSpawnParams( Ax(300) ))
ItemSpawns.append(ItemSpawnParams( Hammer(301) ))
ItemSpawns.append(ItemSpawnParams( Dagger() ))
ItemSpawns.append(ItemSpawnParams( MagicWand(332) ))

# Swords
ItemSpawns.append(ItemSpawnParams( Sword() ))
ItemSpawns.append(ItemSpawnParams( BroadSword() ))
ItemSpawns.append(ItemSpawnParams( LongSword() ))
ItemSpawns.append(ItemSpawnParams( Claymore() ))
ItemSpawns.append(ItemSpawnParams( TwoHandedSword() ))
ItemSpawns.append(ItemSpawnParams( GreatSword() ))

# Rare Weapons
ItemSpawns.append(ItemSpawnParams( ScreamingDagger(322) ))
ItemSpawns.append(ItemSpawnParams( SleepingSword(341) ))
ItemSpawns.append(ItemSpawnParams( FlamingSword(331) ))
ItemSpawns.append(ItemSpawnParams( CrushingHammer(302) ))
ItemSpawns.append(ItemSpawnParams( SlicingAx(303) ))

# Shields
ItemSpawns.append(ItemSpawnParams( BasicShield(311) ))
ItemSpawns.append(ItemSpawnParams( Aegis(312) ))
ItemSpawns.append(ItemSpawnParams( TowerShield(313) ))
ItemSpawns.append(ItemSpawnParams( MagicFocus(314) ))

# Body Armor
ItemSpawns.append(ItemSpawnParams( Chestarmor(600) ))
ItemSpawns.append(ItemSpawnParams( LeatherArmor(601) ))
ItemSpawns.append(ItemSpawnParams( GildedArmor(602) ))
ItemSpawns.append(ItemSpawnParams( WarlordArmor(603) ))
ItemSpawns.append(ItemSpawnParams( WizardRobe(604) ))
ItemSpawns.append(ItemSpawnParams( KarateGi(605) ))
ItemSpawns.append(ItemSpawnParams( BloodstainedArmor(606) ))

# Boots
ItemSpawns.append(ItemSpawnParams( Boots(700) ))
ItemSpawns.append(ItemSpawnParams( BootsOfEscape(701) ))
ItemSpawns.append(ItemSpawnParams( BlackenedBoots(702) ))
ItemSpawns.append(ItemSpawnParams( AssassinBoots(703) ))

# Helmets
ItemSpawns.append(ItemSpawnParams( Helmet(770) ))
ItemSpawns.append(ItemSpawnParams( VikingHelmet(771) ))
ItemSpawns.append(ItemSpawnParams( SpartanHelmet(772) ))
ItemSpawns.append(ItemSpawnParams( ThiefHood(774) ))
ItemSpawns.append(ItemSpawnParams( WizardHat(775) ))

# Gloves
ItemSpawns.append(ItemSpawnParams( Gloves(750) ))
ItemSpawns.append(ItemSpawnParams( Gauntlets(751) ))
ItemSpawns.append(ItemSpawnParams( BoxingGloves(752) ))
ItemSpawns.append(ItemSpawnParams( HealingGloves(753) ))
ItemSpawns.append(ItemSpawnParams( LichHand(754) ))

# Pants
ItemSpawns.append(ItemSpawnParams( Pants(100), minFloor=5, maxFloor=10))

# Rings
ItemSpawns.append(ItemSpawnParams( RingOfSwiftness(500) ))
# ItemSpawns.append(ItemSpawnParams( RingOfTeleportation(505) ))
ItemSpawns.append(ItemSpawnParams( BloodRing(501) ))
ItemSpawns.append(ItemSpawnParams( RingOfMana(502) ))
ItemSpawns.append(ItemSpawnParams( RingOfMight(503) ))
ItemSpawns.append(ItemSpawnParams( BoneRing(504) ))

# Amulets
ItemSpawns.append(ItemSpawnParams( Amulet(550) ))

# Potiorbs
ItemSpawns.append(ItemSpawnParams( HealthPotion(401) ))
ItemSpawns.append(ItemSpawnParams( ManaPotion(402) ))
ItemSpawns.append(ItemSpawnParams( CurePotion(403) ))
ItemSpawns.append(ItemSpawnParams( MightPotion(404) ))
ItemSpawns.append(ItemSpawnParams( DexterityPotion(405) ))
ItemSpawns.append(ItemSpawnParams( PermanentStrengthPotion(404) ))
ItemSpawns.append(ItemSpawnParams( PermanentDexterityPotion(405) ))

# Scrorbs
ItemSpawns.append(ItemSpawnParams( EnchantScrorb(450) ))
ItemSpawns.append(ItemSpawnParams( BurningAttackScrorb(450) ))
#ItemSpawns.append(ItemSpawnParams( TeleportScroll(450), ))
ItemSpawns.append(ItemSpawnParams( MassTormentScroll(450) ))
ItemSpawns.append(ItemSpawnParams( InvincibilityScroll(450) ))
ItemSpawns.append(ItemSpawnParams( CallingScroll(450) ))
#ItemSpawns.append(ItemSpawnParams( SleepScroll(450),      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( ExperienceScroll(450),      1,               10,          5,              5))
ItemSpawns.append(ItemSpawnParams( BlinkScrorb(450) ))
ItemSpawns.append(ItemSpawnParams( MassHealScrorb(450) ))

# Books
#ItemSpawns.append(ItemSpawnParams( BookofMassTorment,      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( BookofMassHeal,      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( BookofSummoning,      1,               10,          1,              1))