#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Post, Tag and Category
"""

from six import with_metaclass
from datetime import datetime

from peanut import pool
from peanut.config import config


class BaseModel(with_metaclass(pool.ObjectPool, object)):
    """Base model"""

    # Pool identity key
    _identity = 'title'

    # layout
    layout = 'page'

    @classmethod
    def all(cls):
        """For pool"""
        pass

    @classmethod
    def get(cls, identity):
        """For pool"""
        pass

    def __init__(self, title, slug):
        self.title = title
        self.slug = slug

    @property
    def url(self):
        path = config.path[self.layout]
        if not path:
            raise KeyError('Path for {} not found'.format(self.layout))
        return path.format(**self.__dict__)


class Post(BaseModel):
    '''Post'''

    layout = 'post'

    def __init__(self, title, slug, content=None, date=None,
                 publish=True, top=False, layout='post', tags=None, category=None):

        super(Post, self).__init__(title=title, slug=title)

        self.content = content
        self.date = date or datetime.now()
        self.top = top
        self.publish = publish
        self.layout = layout
        self._tags = set()
        self._category = None

        if tags:
            for tag in tags:
                self.add_tag(tag)

        if category:
            self.category = category

    def add_tag(self, tag):
        """Add tag"""
        self._tags.add(tag.title)

    @classmethod
    def top_posts(cls):
        """Get all top posts"""
        return filter(lambda p: p.top, cls.all())

    @property
    def tags(self):
        """Get all tags"""
        return [Tag.get(tag) for tag in self._tags]

    @property
    def catetory(self):
        return Category.get(self._category)

    @catetory.setter
    def category(self, value):
        if value:
            self._category = value.title
        else:
            self._category = None


class Tag(BaseModel):
    """Tag"""

    layout = 'tag'

    def __init__(self, title):
        super(Tag, self).__init__(title=title, slug=title)

    @property
    def posts(self):
        """Get all posts that have this tag"""
        return filter(lambda p: self.title in p._tags, Post.all())


class Category(Tag):
    """Category"""

    layout = 'category'

    @property
    def posts(self):
        """Get all posts that belongs to this category"""
        return filter(lambda p: p._category==self.title, Post.all())
