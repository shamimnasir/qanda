#!/bin/bash
# Create a new documentary project from the skill's engine.
# Usage: bash new_project.sh "Project Name" [parent folder]   -> <parent>/Project_Name_Documentary
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
ENG="$SKILL/assets/engine"; TPL="$SKILL/assets/templates"
CACHE="$HOME/.cache/documentary-studio/remotion"
NAME="$1"; [ -z "$NAME" ] && { echo 'usage: bash new_project.sh "Project Name" [parent folder]'; exit 1; }
PARENT="$(cd "${2:-.}" && pwd)"
SLUG=$(echo "$NAME" | tr ' ' '_' | tr -cd '[:alnum:]_')
DEST="$PARENT/${SLUG}_Documentary"
[ -e "$DEST" ] && { echo "already exists: $DEST"; exit 1; }
mkdir -p "$DEST"/{01_Script,02_Footage_Licensed/originals,03_Images/commons,04_AI_Generated,05_Motion_Graphics/thumbnails,06_Audio_Voiceover,07_Music_SFX,09_Permissions_and_Licenses}
mkdir -p "$DEST"/08_Timeline_and_Exports/{data,renders/stills,review}
cp -R "$ENG/scripts" "$DEST/08_Timeline_and_Exports/scripts"
cp -R "$ENG/remotion" "$DEST/08_Timeline_and_Exports/remotion"
if [ -d "$CACHE/node_modules" ]; then
  cp -cR "$CACHE/node_modules" "$DEST/08_Timeline_and_Exports/remotion/node_modules" 2>/dev/null || cp -R "$CACHE/node_modules" "$DEST/08_Timeline_and_Exports/remotion/node_modules"
else
  echo "Note: Remotion packages are not cached yet. Run: bash \"$SKILL/scripts/setup.sh\" --install"
fi
cp "$ENG/studio.sh" "$DEST/studio.sh"; chmod +x "$DEST/studio.sh"
sed -e "s/__TITLE__/$NAME/g" -e "s/__SLUG__/$SLUG/g" "$TPL/project.template.json" > "$DEST/project.json"
sed -e "s|__SKILL__|$SKILL|g" "$SKILL/assets/project_CLAUDE.md" > "$DEST/CLAUDE.md"
cp "$TPL/script_master.template.tsv" "$DEST/01_Script/script_master.tsv"
cp "$TPL/shotlist.template.json" "$DEST/08_Timeline_and_Exports/data/shotlist.json"
mkdir -p "$DEST/05_Motion_Graphics/producer"; cp "$SKILL/assets/producer/"*.webp "$SKILL/assets/producer/README.md" "$DEST/05_Motion_Graphics/producer/"
cp "$TPL/thumbnails.template.json" "$DEST/08_Timeline_and_Exports/data/thumbnails.json"
cp "$TPL/facts_to_verify.template.md" "$DEST/01_Script/facts_to_verify.md"
sed -e "s/__TITLE__/$NAME/g" "$TPL/demand_brief.template.md" > "$DEST/01_Script/demand_brief.md"
cp "$TPL/demand_research.template.csv" "$DEST/01_Script/demand_research.csv"
mkdir -p "$DEST/11_Performance"
mkdir -p "$PARENT/_Channel"
[ -e "$PARENT/_Channel/channel_strategy.md" ] || cp "$TPL/channel_strategy.template.md" "$PARENT/_Channel/channel_strategy.md"
[ -e "$PARENT/_Channel/learned_rules.md" ] || cp "$TPL/learned_rules.template.md" "$PARENT/_Channel/learned_rules.md"
cp "$TPL/publish_kit.template.md" "$DEST/08_Timeline_and_Exports/youtube_publish_kit.md"
cp "$TPL/permission_request.template.md" "$DEST/09_Permissions_and_Licenses/permission_request_template.md"
echo 'shot_id,script_timestamp,chapter,description,source_type,source_site,asset_url_or_file_name,creator,license_type,commercial_use_allowed,attribution_text_required,cost,status,notes' > "$DEST/tracker.csv"
echo '{}' > "$DEST/08_Timeline_and_Exports/data/picks.json"
KEYFILE="$HOME/.config/documentary-studio/.env"
if [ -f "$KEYFILE" ]; then (umask 077; cp "$KEYFILE" "$DEST/.env")
elif [ -n "$PEXELS_API_KEY" ]; then (umask 077; echo "PEXELS_API_KEY=$PEXELS_API_KEY" > "$DEST/.env")
else echo "Note: no Pexels key found. Run: bash \"$SKILL/scripts/setup.sh\" --key"; fi
echo "Created $DEST"
echo "Next: fill 01_Script/script_master.tsv and project.json, then ./studio.sh scripts"
