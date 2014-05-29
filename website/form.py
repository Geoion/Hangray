# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class RegisterForm(forms.Form):
    email = forms.EmailField(label=_(u"邮件"), max_length=30,
                             widget=forms.TextInput(
                                 attrs={'size': 30, 'class': 'form-control', 'placeholder': '您的邮箱', }))
    password = forms.CharField(label=_(u"密码"), max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'size': 20, 'class': 'form-control', 'placeholder': '您的密码', }))
    username = forms.CharField(label=_(u"昵称"), max_length=30,
                               widget=forms.TextInput(
                                   attrs={'size': 20, 'class': 'form-control', 'placeholder': '您的姓名', }))

    def clean_username(self):
        """验证重复昵称"""
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"该昵称已经被使用请使用其他的昵称"))

    def clean_email(self):
        """验证重复email"""
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"该邮箱已经被使用请使用其他的"))


class LoginForm(forms.Form):
    email = forms.CharField(label=_(u"邮箱"), max_length=30,
                            widget=forms.TextInput(
                                attrs={'size': 20, 'class': 'form-control', 'placeholder': '您的邮箱'}))
    password = forms.CharField(label=_(u"密码"), max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'size': 20, 'class': 'form-control', 'placeholder': '您的密码'}))


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """

    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class EditInfoForm(forms.Form):
    upload_image = forms.FileField(label='选择你的头像上传')
    short_introduce = forms.CharField(max_length=50,
                                      widget=forms.TextInput(
                                          attrs={'size': 20, 'class': 'form-control', 'placeholder': '一句话介绍你自己'}))
    introduce = forms.CharField(label=_(u"介绍"), max_length=200,
                                widget=forms.Textarea(
                                    attrs={'size': 20, 'class': 'form-control', 'placeholder': '详细的介绍你自己',
                                           'rows': '4'}))
    sex = forms.ChoiceField(choices=(('男', '男'), ('女', '女')), widget=forms.Select(attrs={'class': 'form-control'}))
    industry = forms.ChoiceField(choices=(('互联网', '互联网'), ('金融', '金融'), ('制造', '制造'),
                                          ('管理', '管理'), ('服务', '服务'), ),
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(label=_(u'city'), max_length=20,
                           widget=forms.TextInput(
                               attrs={'size': 20, 'class': 'form-control', 'placeholder': '居住地'}))
    phone_number = forms.CharField(label=_(u'电话'), max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'size': 30, 'class': 'form-control', 'placeholder': '您的电话', }))


class QuestionForm(forms.Form):
    title = forms.CharField(label=_(u'title'), max_length=50,
                            widget=forms.TextInput(
                                attrs={'size': 20, 'class': 'form-control', 'placeholder': '问题标题'}
                            ))
    content = forms.CharField(label=_(u"content"), max_length=200,
                              widget=forms.Textarea(
                                  attrs={'size': 20, 'class': 'form-control', 'placeholder': '题目详细描述',
                                         'rows': '4'}
                              ))
    topic = forms.CharField(label=_(u'topic'), max_length=50,
                            widget=forms.TextInput(
                                attrs={'size': 20, 'class': 'form-control', 'placeholder': '话题'}
                            ))

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        return cleaned_data


class AnswerForm(forms.Form):
    content = forms.CharField(label=_(u"content"), max_length=500,
                              widget=forms.Textarea(
                                  attrs={'size': 20, 'class': 'form-control', 'placeholder': '这里输入你的答案',
                                         'rows': '5'}
                              ))


class CommentForm(forms.Form):
    content = forms.CharField(label=_(u'title'), max_length=50,
                              widget=forms.TextInput(
                                  attrs={'size': 20, 'class': 'form-control', 'placeholder': '评论'}
                              ))