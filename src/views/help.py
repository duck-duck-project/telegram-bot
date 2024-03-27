from views.base import View

__all__ = ('HelpView',)


class HelpView(View):
    text = (
        '📚 Справочник по боту:'
        ' <a href="https://graph.org/Duck-Duck-FAQ-03-27">*ссылка*</a>'
    )
