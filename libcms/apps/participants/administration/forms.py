# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from accounts.models import GroupTitle

from ..models import Library, LibraryType, District, UserLibrary, UserLibraryPosition, get_role_groups


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = ('parent',)


class LibraryTypeForm(forms.ModelForm):
    class Meta:
        model = LibraryType
        exclude = []


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        exclude = []


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=64, label=u'Пароль *', required=False)
    email = forms.EmailField(label=u'Адрес электронной почты', help_text=u'Только в домене @tatar.ru ')
    last_name = forms.CharField(label=u'Фамилия', max_length=30)
    first_name = forms.CharField(label=u'Имя', max_length=30)

    class Meta:
        model = User
        fields = ['email', 'password', 'last_name', 'first_name']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        # if not email.endswith('@tatar.ru'):
        #     raise forms.ValidationError(u'Адрес электронной почты должен заканчиваться на @tatar.ru')
        if self.instance.email != email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'Такой адрес уже зарегистрирован')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.instance.pk and not password:
            raise forms.ValidationError(u'Укажите или сгенерируйте пароль')
        return password


class UserLibraryForm(forms.ModelForm):
    class Meta:
        model = UserLibrary
        exclude = ('library', 'user')
        widgets = {
            'roles': forms.CheckboxSelectMultiple()
        }


def get_role_choices():
    groups = Group.objects.filter(name__startswith='role_')
    group_titles = GroupTitle.objects.filter(group__in=groups)

    group_titles_dict = {}

    for group_title in group_titles:
        group_titles_dict[group_title.group_id] = group_title.title
    choices = []
    for group in groups:
        choices.append(
            (group.id, group_titles_dict.get(group.id, group.name))
        )
    return choices


class UserLibraryGroupsFrom(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLibraryGroupsFrom, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.MultipleChoiceField(
            label=u'Группы',
            choices=get_role_choices(),
            widget=forms.CheckboxSelectMultiple
        )


def get_district_form(districts=None):
    if not districts:
        queryset = District.objects.all()
    else:
        queryset = District.objects.filter(id__in=districts)

    class SelectDistrictForm(forms.Form):
        district = forms.ModelChoiceField(queryset=queryset, label=u'Выберите район', required=False)

    return SelectDistrictForm


class SelectUserPositionForm(forms.Form):
    position = forms.ModelChoiceField(queryset=UserLibraryPosition.objects.all(), label=u'Должность', required=False)


class SelectUserRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.filter(name__startswith='role_'), label=u'Роль', required=False)



class UserAttrForm(forms.Form):
    fio = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'ФИО'})
    )
    login = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'Логин'})
    )
    email = forms.CharField(
        label=u'',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': u'Email'})
    )


def get_add_user_library_form(queryset=None):
    if not queryset:
        queryset = Library.objects.all()

    class AddUserDistrictForm(forms.Form):
        library = forms.ModelChoiceField(
            queryset=queryset,
            label=u'Выберите библиотеку'
        )

    return AddUserDistrictForm


# class UserLibrary(forms.ModelForm):
# class Meta:
# model = UserLibrary
# exclude = ('library',)


# from pages.models import Page, Content
#
# class PageForm(forms.ModelForm):
# class Meta:
# model=Page
#        exclude = ('parent',)
#
#class ContentForm(forms.ModelForm):
#    class Meta:
#        model=Content
#        exclude = ('page',)
#
#
#
#def get_content_form(exclude_list = ('page',)):
#    class ContentForm(forms.ModelForm):
#        class Meta:
#            model=Content
#            exclude = exclude_list
#    return ContentForm

