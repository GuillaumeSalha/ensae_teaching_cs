"""
@brief      test log(time=2s)

"""


import sys
import os
import unittest
import pandas
import datetime


try:
    import src
    import pyquickhelper as skip_____
    import pyensae as skip___
    import pyrsslocal as skip__
    import pymyinstall as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pymyinstall",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyrsslocal",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pymmails",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip____
    import pyensae as skip___
    import pyrsslocal as skip__
    import pymmails as skip_

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from pymmails import MailBoxMock, EmailMessageRenderer, EmailMessageListRenderer
from pymmails.render.email_message_style import template_email_html_short
from src.ensae_teaching_cs.automation_students import ProjectsRepository


class TestRepository(unittest.TestCase):

    def test_sections(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        data = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(data, "data")
        dfile = os.path.join(data, "notes_eleves_2104_2015.xlsx")
        df = pandas.read_excel(dfile, skiprows=5)
        df = df[df["Groupe"] != "moyenne"].copy()
        fLOG(df.columns)
        fLOG(df.tail())
        fLOG(df.shape)
        emails = ["firstname.ABOUT@machin.fr".lower(),
                  "one_name.another_name.third.fourth@machin.fr"]
        temp = get_temp_folder(__file__, "temp_repository")
        try:
            proj = ProjectsRepository.create_folders_from_dataframe(df, temp, col_subject="sujet",
                                                                    fLOG=fLOG, col_group=None,
                                                                    email_function=emails,
                                                                    skip_if_nomail=True)
        except ProjectsRepository.MailNotFound:
            pass

        emails = ["firstname.ABOUT@machin.fr".lower(), "firstname.SECOND@hhh.fr",
                  "one_name.another_name.third.fourth@machin.fr"]

        proj = ProjectsRepository.create_folders_from_dataframe(df, temp, col_subject="sujet",
                                                                fLOG=fLOG, col_group=None,
                                                                email_function=emails,
                                                                must_have_email=False)

        if True:
            data = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "data"))
            box = MailBoxMock(data, b"unittestunittest", fLOG)
            box.login()

            email_render = EmailMessageRenderer(
                tmpl=template_email_html_short, fLOG=fLOG)
            render = EmailMessageListRenderer(title="list of mails",
                                              email_renderer=email_render, fLOG=fLOG)

            mails = proj.dump_group_mails(render, group=None,
                                          mailbox=box, subfolder="trav",
                                          date=datetime.datetime(2015, 1, 9))

            box.logout()

        suivi = os.path.join(temp, "ABOUT.firstname", "suivi.rst")
        with open(suivi, "r", encoding="utf8") as f:
            content = f.read()
        self.assertIn("* mails: firstname.about@machin.fr", content)

        self.assertEqual(len(proj.Groups), 3)
        mails = proj.get_emails(proj.Groups[0])
        self.assertEqual(mails, ['firstname.about@machin.fr'])
        fLOG("------", os.path.exists(os.path.join(temp, "mail_style.css")))
        proj.write_summary()
        fLOG("------")
        files = [os.path.join(temp, "index.html"),
                 os.path.join(
                     temp, "ABOUT.firstname", "d_2015-08-01_p_noreply-at-voyages-sncf-com_ii_8de6a63addb7c03407bc6f0caabd967e.html"),
                 os.path.join(temp, "mail_style.css")]
        nb = 0
        for name in files:
            if not os.path.exists(name):
                raise FileNotFoundError(name)
            nb += 1
            with open(name, "r", encoding="utf8") as f:
                content = f.read()
            self.assertNotIn("ut_automation_students", content)
        self.assertEqual(nb, len(files))


if __name__ == "__main__":
    unittest.main()
