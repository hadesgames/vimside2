import os
import vimside
import vimside.ensime.command
import tempfile
import tests.ensime
class TestClasspath(tests.ensime.EnsimeTestCase):

    @classmethod
    def _key(cls, section, option):
        return "%s|%s" % (section, option)

    @classmethod
    def _unkey(cls, key):
        return key.split("|")


    def _set(self, section, option, value):
        orig = vimside.config.get(section, option)
        self._originals[self._key(section, option)] = orig
        vimside.config.set(section, option, value)


    def setUp(self):
        self._originals = {}
        self._tmp = tempfile.mkdtemp()

        self._set('vimside', 'cache-dir', self._tmp)

    def tearDown(self):
        for key, value in self._originals.iteritems():
            section, option = self._unkey(key)
            vimside.config.set(section, option, value)

    def test_can_create_classpath(self):
        vimside.ensime.command.classpath()

        classpath_dir = os.path.join(
            self._tmp,
            vimside.config.get('vimside', 'classpath-cache'))

        files = os.listdir(classpath_dir)

        self.assertEqual(len(files), 1)

        cp = None
        with open(os.path.join(classpath_dir, files[0])) as fh:
            cp = fh.read()

        self.assertIsInstance(cp, str)
        self.assertGreater(len(cp), 0)

    def test_caches_classpath(self):
        classpath_dir = os.path.join(
            self._tmp,
            vimside.config.get('vimside', 'classpath-cache'))

        os.mkdir(classpath_dir)

        classpath_file = os.path.join(classpath_dir, 'CLASSPATH_%s_%s' % (
            vimside.config.get('ensime', 'scala-version'),
            vimside.config.get('ensime', 'ensime-version')))

        print classpath_file

        with open(classpath_file, 'w') as fh:
            fh.write('/tmp/test')

        vimside.ensime.command.classpath()

        classpath_dir = os.path.join(
            self._tmp,
            vimside.config.get('vimside', 'classpath-cache'))

        files = os.listdir(classpath_dir)

        self.assertEqual(len(files), 1)

        cp = None
        with open(os.path.join(classpath_dir, files[0])) as fh:
            cp = fh.read()

        self.assertEqual(cp, '/tmp/test')
