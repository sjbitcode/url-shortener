from django.test import TestCase

from links.models import Link, Tag


class TagUtilsTest(TestCase):
    def test_one_whitespace_string(self):
        '''
        Test normalize_text method with
        one whitespace.
        '''

        text = Tag.normalize_text(' ')
        self.assertEqual(text, '')

    def test_multiple_whitespace_string(self):
        '''
        Test normalize_text method with
        strings with 2 whitespaces and
        10 whitespaces.
        '''

        text1 = Tag.normalize_text('  ')
        text2 = Tag.normalize_text('          ')

        self.assertEqual(text1, '')
        self.assertEqual(text2, '')

    def test_empty_string(self):
        '''
        Test normalize_text method with
        empty string.
        '''

        text = Tag.normalize_text('')
        self.assertEqual(text, None)

    def test_left_whitespace_string(self):
        '''
        Test a string with whitspaces to left.
        '''

        text = Tag.normalize_text('   tag')
        self.assertEqual(text, 'tag')

    def test_right_whitespace_string(self):
        '''
        Test a string with whitespaces to right.
        '''

        text = Tag.normalize_text('tag   ')
        self.assertEqual(text, 'tag')

    def test_non_alnumeric_string(self):
        '''
        Test a series of strings with
        non-alphanumeric characters excluding dashes.
        '''

        text1 = Tag.normalize_text('__init__(*args, **kwargs):')
        text2 = Tag.normalize_text('# This is a comment')
        text3 = Tag.normalize_text('Hello!')
        text4 = Tag.normalize_text('4^2')
        text5 = Tag.normalize_text('Total is $2.99')
        text6 = Tag.normalize_text('tag_name_')
        text7 = Tag.normalize_text('. . .')
        text8 = Link.normalize_key('(')
        text9 = Link.normalize_key(')')

        self.assertEqual(text1, None)
        self.assertEqual(text2, None)
        self.assertEqual(text3, None)
        self.assertEqual(text4, None)
        self.assertEqual(text5, None)
        self.assertEqual(text6, None)
        self.assertEqual(text7, None)
        self.assertEqual(text8, None)
        self.assertEqual(text9, None)

    def test_spaces_inbetween_string(self):
        '''
        Test strings with multiple
        whitespaces in between words.
        '''

        text1 = Tag.normalize_text('sky is blue')
        text2 = Tag.normalize_text('two  spaces  between  words')
        text3 = Tag.normalize_text('this is      a   tag')

        self.assertEqual(text1, 'sky-is-blue')
        self.assertEqual(text2, 'two-spaces-between-words')
        self.assertEqual(text3, 'this-is-a-tag')

    def test_uppercase_string(self):
        text1 = Tag.normalize_text('The sky is blue')
        text2 = Tag.normalize_text('THE SKY IS BLUE')
        text3 = Tag.normalize_text('aAbbcCdDeEfFgG')

        self.assertEqual(text1, 'the-sky-is-blue')
        self.assertEqual(text2, 'the-sky-is-blue')
        self.assertEqual(text3, 'aabbccddeeffgg')

    def test_dashes_string(self):
        text1 = Tag.normalize_text('-')
        text2 = Tag.normalize_text('--')
        text3 = Tag.normalize_text('--------')
        text4 = Tag.normalize_text(' - ')
        text5 = Tag.normalize_text('-tag-')
        text6 = Tag.normalize_text('-tag-name-')
        text7 = Tag.normalize_text('- tag - name -')
        text8 = Tag.normalize_text('tag  -- - name - ')

        self.assertEqual(text1, '')
        self.assertEqual(text2, '')
        self.assertEqual(text3, '')
        self.assertEqual(text4, '')
        self.assertEqual(text5, 'tag')
        self.assertEqual(text6, 'tag-name')
        self.assertEqual(text7, 'tag-name')
        self.assertEqual(text8, 'tag-name')


class LinkUtilsTest(TestCase):
    def test_empty_string(self):
        '''
        Test normalize_key method with
        empty string.
        '''

        text = Link.normalize_key('')
        self.assertEqual(text, None)

    def test_one_whitespace_string(self):
        '''
        Test normalize_key method with
        one whitespace.
        '''

        text = Link.normalize_key(' ')
        self.assertEqual(text, None)

    def test_multiple_whitespace_string(self):
        '''
        Test normalize_key method with
        strings with 2 whitespaces and
        10 whitespaces.
        '''

        text1 = Link.normalize_key('  ')
        text2 = Link.normalize_key('          ')

        self.assertEqual(text1, None)
        self.assertEqual(text2, None)

    def test_left_whitespace_string(self):
        '''
        Test a string with whitspaces to left.
        '''

        text = Link.normalize_key('   key')
        self.assertEqual(text, None)

    def test_right_whitespace_string(self):
        '''
        Test a string with whitespaces to right.
        '''

        text = Link.normalize_key('key   ')
        self.assertEqual(text, None)

    def test_non_alnumeric_string(self):
        '''
        Test a series of strings with
        non-alphanumeric characters excluding dashes.
        '''

        text1 = Link.normalize_key('__init__(*args, **kwargs):')
        text2 = Link.normalize_key('# This is a comment')
        text3 = Link.normalize_key('Hello!')
        text4 = Link.normalize_key('4^2')
        text5 = Link.normalize_key('Total is $2.99')
        text6 = Link.normalize_key('tag_name_')
        text7 = Link.normalize_key('. . .')
        text8 = Link.normalize_key('abc123%')
        text9 = Link.normalize_key('(')
        text10 = Link.normalize_key(')')

        self.assertEqual(text1, None)
        self.assertEqual(text2, None)
        self.assertEqual(text3, None)
        self.assertEqual(text4, None)
        self.assertEqual(text5, None)
        self.assertEqual(text6, None)
        self.assertEqual(text7, None)
        self.assertEqual(text8, None)
        self.assertEqual(text9, None)
        self.assertEqual(text10, None)

    def test_spaces_inbetween_string(self):
        '''
        Test strings with multiple
        whitespaces in between words.
        '''

        text1 = Link.normalize_key('the sky is blue')
        text2 = Link.normalize_key('my age is 25')

        self.assertEqual(text1, None)
        self.assertEqual(text2, None)

    def test_uppercase_string(self):
        '''
        Test strings with uppercase characters.
        '''

        text1 = Link.normalize_key('Hello')
        text2 = Link.normalize_key('HellO')
        text3 = Link.normalize_key('HELLO')

        self.assertEqual(text1, 'Hello')
        self.assertEqual(text2, 'HellO')
        self.assertEqual(text3, 'HELLO')

    def test_dashes_string(self):
        '''
        Test strings with dashes.
        '''

        text1 = Link.normalize_key('-')
        text2 = Link.normalize_key('--')
        text3 = Link.normalize_key('hello-there')
        text4 = Link.normalize_key('hello--there')
        text5 = Link.normalize_key('-hello-there-')
        text6 = Link.normalize_key('--hello--there--')

        self.assertEqual(text1, None)
        self.assertEqual(text2, None)
        self.assertEqual(text3, 'hello-there')
        self.assertEqual(text4, 'hello-there')
        self.assertEqual(text5, 'hello-there')
        self.assertEqual(text6, 'hello-there')
