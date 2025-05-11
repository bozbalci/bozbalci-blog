from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes

from notcms.settings.base import WAGTAILADMIN_RICH_TEXT_EDITORS

WAGTAIL_RICH_TEXT_EDITOR_FEATURES = WAGTAILADMIN_RICH_TEXT_EDITORS["default"][
    "OPTIONS"
]["features"]


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("", "Plain text"),
            ("bash", "Bash/Shell"),
            ("python", "Python"),
        ],
        required=False,
        help_text="Language for syntax highlighting",
    )
    code = blocks.TextBlock()

    class Meta:
        template = "blocks/code.html"
        icon = "code"
        label = "Code"
        form_classname = "code-block struct-block"


class SummaryDetailsBlock(blocks.StructBlock):
    summary = blocks.CharBlock(required=True, help_text="Text shown in the summary")
    details = blocks.StreamBlock(
        [("paragraph", blocks.RichTextBlock()), ("code", CodeBlock())]
    )

    class Meta:
        template = "blocks/summary_details.html"
        icon = "user"
        form_classname = "summary-details-block struct-block"


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageBlock(required=True)
    caption = blocks.RichTextBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/captioned_image.html"


class CommonPostBodyBlock(blocks.StreamBlock):
    blockquote = blocks.BlockQuoteBlock()
    paragraph = RichTextBlockWithFootnotes(features=WAGTAIL_RICH_TEXT_EDITOR_FEATURES)
    image = ImageBlock()
    captioned_image = CaptionedImageBlock()
    code = CodeBlock()
    details = SummaryDetailsBlock()
