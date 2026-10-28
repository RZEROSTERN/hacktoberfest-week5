# Authored story rules

- canon.json, objects.json, endings.json and lines.json are the story's source of truth.
- All player-facing prose must exist in both English and Spanish, with matching meaning.
- Inés and her household are original fiction. Never add real likenesses or imply a
  single fictional story defines Día de los Muertos for all families or communities.
- A memory can be recovered in any order; clues must not require hidden biographical facts.
- Keep life facts, names, dates, places, relationships and reveal references consistent.
- Every object needs unrecovered/connected/recovered/unrelated/redirect/error fallbacks.
- All/some/no-memory endings stay authored and gentle; code chooses the ending.
- The owner must approve the full story before its PR opens. Passing data checks is
  not approval. Do not change review_status to approved without the owner's response.
- After edits: `node scripts/story-review.mjs`, then `npm run check`. Review the
  complete docs/STORY_REVIEW.md, including both languages and fallback dialogue.
