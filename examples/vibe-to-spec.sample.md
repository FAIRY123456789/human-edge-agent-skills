# Vibe to Spec — Sample

## Active project glossary

- 澄舟台：虚构的当前项目名称
- Topic Shift：话题切换检测

## Raw ASR-style input

> 我们把成舟台那个聊天页改一下，就是左边导航别动，然后我想把话题切换那个东西加进去，用户如果已经从海报聊到视频了就不要还拿着前面的海报参数。然后导出那块千万不要动，之前有问题好不容易修好。这个先做后端还是前端我不管，你自己判断，但是最后要给我能验收的东西。

## Expected normalization

High-confidence correction:

`成舟台` → `澄舟台`

Reason: canonical project name is explicitly present in the active glossary; phonetic similarity is high; semantic role matches a project/product name.

## Expected spec excerpt

### Goal

Add topic-shift-aware context handling to the existing chat workflow while preserving the current left navigation and export behavior.

### Out of scope

- Redesigning the left navigation.
- Changing export logic.

### Acceptance criteria

1. When the user changes from one content topic to another, incompatible prior-topic fields are not carried into the new request.
2. Existing export behavior is unchanged under regression tests.
3. The implementation includes a reproducible test covering at least one topic-shift case.
