"""
Rate my professor python API.
"""
import re
import requests
import time

from lxml import etree

#Author Email: yiyangl6@asu.edu

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.142 Safari/537.36"
}

INFO_NOT_AVAILABLE = "Info currently not available"

TEACHER_LIST = []
TAG_FEEDBACK_LIST = []
RATING_LIST = []
NAME_LIST = []
DEPARTMENT_LIST = []
DIFFICULTY_LIST = []
TAKE_AGAIN_LIST = []

class RateMyProfAPI:
    """
    School id 45 = Arizona State University, the ID is initialized to 45 if not set upon usage.
    """
    def __init__(self, school_id=45, teacher="staff", callback=None):
        """
        Initialize the rate my professor API.
        :param school_id: int, default: 45.
               The school code for where you want the professor's name to be checked.

        :param teacher: teacher's full name. if the teacher's name is not available,
                        default will be staff.
        """
        self.reset()

        if teacher != "staff":
            teacher = str(teacher).replace(" ", "+")
        else:
            teacher = ""

        self.teacher_name = teacher
        if self.teacher_name in TEACHER_LIST:
            self.index = TEACHER_LIST.index(self.teacher_name)
        else:
            TEACHER_LIST.append(self.teacher_name)

        self.callback = callback
        self.school_id = school_id
        self.school_name = self._get_school_name()

    def reset(self):
        self.page_data = ""
        self.tag_feed_back = ""
        self.rating = ""
        self.name = ""
        self.department = ""
        self.difficulty = ""
        self.take_again = ""
        self.index = -1

    def _get_school_name(self) -> str:
        url = f'https://www.ratemyprofessors.com/campusRatings.jsp?sid={self.school_id}'
        page = requests.get(url, headers=headers)
        school_name_node = re.findall(r"schoolName: '(.*?)'", page.text)
        if school_name_node:
            school_name: str = school_name_node[0]
        else:
            raise ValueError('Invalid school id!')

        school_name = school_name.replace(' ', '+')
        return school_name

    def retrieve_rmp_info(self):
        """
        :function: initialize the RMP data
        """

        #If professor showed as "staff"
        # if self.teacher_name == "":
            # self.rating = INFO_NOT_AVAILABLE
            # self.department = INFO_NOT_AVAILABLE
            # self.difficulty = INFO_NOT_AVAILABLE
            # self.name = INFO_NOT_AVAILABLE
            # self.take_again = INFO_NOT_AVAILABLE
            # self.tag_feed_back = []

            # RATING_LIST.append(INFO_NOT_AVAILABLE)
            # DEPARTMENT_LIST.append(INFO_NOT_AVAILABLE)
            # DIFFICULTY_LIST.append(INFO_NOT_AVAILABLE)
            # NAME_LIST.append(INFO_NOT_AVAILABLE)
            # TAKE_AGAIN_LIST.append(INFO_NOT_AVAILABLE)
            # TAG_FEEDBACK_LIST.append(INFO_NOT_AVAILABLE)

            # return

        # if self.index == -1:
            #making request to the RMP page
        self._retrieve_rmp_info()
        RATING_LIST.append(self.rating)
        DEPARTMENT_LIST.append(self.department)
        DIFFICULTY_LIST.append(self.difficulty)
        NAME_LIST.append(self.name)
        TAKE_AGAIN_LIST.append(self.take_again)
        TAG_FEEDBACK_LIST.append(self.tag_feed_back)

        # else:
            # self.rating = RATING_LIST[self.index]
            # self.department = DEPARTMENT_LIST[self.index]
            # self.difficulty = DIFFICULTY_LIST[self.index]
            # self.name = NAME_LIST[self.index]
            # self.take_again = TAKE_AGAIN_LIST[self.index]
            # self.tag_feed_back = TAG_FEEDBACK_LIST[self.index]

    def _retrieve_rmp_info(self):
        offset = 0

        while True:
            url = f"https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&" \
                  f"queryBy=teacherName" \
                  f"&schoolName={self.school_name}" \
                  f"&schoolID={self.school_id}&query={self.teacher_name}" \
                  f"&max=20&offset={offset}"

            page = requests.get(url=url, headers=headers)
            self.page_data = page.text
            page_data_temp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.page_data)
            if page_data_temp:
                page_data_temp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.page_data)
                if self.callback:
                    for teacher in page_data_temp:
                        self._retrieve_rmp_info_for_teacher(teacher)
                        self.callback(self)
                        time.sleep(2)
                else:
                    self._retrieve_rmp_info_for_teacher(page_data_temp[0])
                    break
            else:
                self.rating = INFO_NOT_AVAILABLE
                self.department = INFO_NOT_AVAILABLE
                self.difficulty = INFO_NOT_AVAILABLE
                self.name = INFO_NOT_AVAILABLE
                self.take_again = INFO_NOT_AVAILABLE
                self.tag_feed_back = []
                break

            offset = offset + 20

    def _retrieve_rmp_info_for_teacher(self, page_data_temp):
        final_url = "https://www.ratemyprofessors.com/" + page_data_temp
        self.tag_feed_back = []

        page = requests.get(final_url)
        document = etree.HTML(page.text)

        try:
            # Get tags
            tags = document.xpath(
                '//*[@id="root"]/div/div/'
                'div[3]/div[4]/div[1]/div[1]/ul/li/div/div/div[3]/div[4]/span/text()'
            )
            tags = map(lambda x: x.lower(), tags)

            if not tags:
                self.tag_feed_back = []
            else:
                self.tag_feed_back = tags
        except:
            pass
        try:
            # Get name
            self.name = self._get_name(document)
        except:
            pass
        try:
            # Get rating
            self.rating = self._get_rating(document)
        except:
            pass
        try:
            # Get department
            self.department = self._get_department(document)
        except:
            pass
        try:
            # Get difficulty
            self.difficulty = self._get_difficulty(document)
        except:
            pass
        try:
            # Get "Would Take Again" Percentage
            take_again = document.xpath(
                '//*[@id="root"]/div/div/div[3]/div[1]'
                '/div[1]/div[3]/div[1]/div[1]/text()'
            )

            if not take_again:
                self.take_again = INFO_NOT_AVAILABLE
            else:
                take_again = re.findall(r'\d+%', take_again[0])
                if not take_again:
                    self.take_again = INFO_NOT_AVAILABLE
                else:
                    self.take_again = take_again[0]
        except:
            pass

    def _get_rating(self, document) -> str:
        rating = document.xpath(
            '//*[@id="root"]/div/div/'
            'div[3]/div[1]/div[1]/div[1]/div[1]/'
            'div/div[1]/text()'
        )[0]

        if not re.match(r'.*?N/A', self.rating):
            rating = re.findall(r'\d\.\d', rating)
            if not rating:
                rating = INFO_NOT_AVAILABLE
            else:
                rating = rating[0]

            return rating

        return INFO_NOT_AVAILABLE

    def _get_name(self, document) -> str:
        name = document.xpath(
            '//*[@id="root"]/div/div/div[3]/div[1]'
            '/div[1]/div[2]/div[1]/span/text()'
        )
        name = " ".join(name)

        if not re.match(r'.*?N/A', self.name):
            return name

        return INFO_NOT_AVAILABLE

    def _get_department(self, document) -> str:
        department = document.xpath(
            '//*[@id="root"]/div/div/div[3]/div[1]'
            '/div[1]/div[2]/div[2]/span/b/text()'
        )[0]

        if not re.match(r'.*?N/A', self.department):
            return department

        return INFO_NOT_AVAILABLE

    def _get_difficulty(self, document) -> str:
        difficulty = document.xpath(
            '//*[@id="root"]/div/div/div[3]/div[1]'
            '/div[1]/div[3]/div[2]/div[1]/text()'
        )[0]

        if not re.match(r'.*?N/A', self.difficulty):
            difficulty = re.findall(r'\d\.\d', difficulty)
            if not difficulty:
                difficulty = INFO_NOT_AVAILABLE
            else:
                difficulty = difficulty[0]

            return difficulty

        return INFO_NOT_AVAILABLE

    def get_school_name(self):
        school_name = self.school_name.replace('+', ' ')
        return school_name

    def get_school_id(self):
        return self.school_id

    def get_rating(self):
        """
        :return: RMP rating.
        """
        return INFO_NOT_AVAILABLE if self.rating == INFO_NOT_AVAILABLE else self.rating

    def get_name(self):
        """
        :return: Professor name.
        """
        return INFO_NOT_AVAILABLE if self.name == INFO_NOT_AVAILABLE else self.name

    def get_department(self):
        """
        :return: RMP department.
        """
        return INFO_NOT_AVAILABLE if self.department == INFO_NOT_AVAILABLE else self.department

    def get_difficulty(self):
        """
        :return: RMP difficulty.
        """
        return INFO_NOT_AVAILABLE if self.difficulty == INFO_NOT_AVAILABLE else self.difficulty

    def get_tags(self):
        """
        :return: teacher's tag in [list]
        """
        return set(self.tag_feed_back)

    def get_first_tag(self):
        """

        :return: teacher's most popular tag [string]
        """
        try:
            if self.tag_feed_back and len(list(self.tag_feed_back)) > 0:
                return list(self.tag_feed_back)[0]
            return INFO_NOT_AVAILABLE
        except:
            return INFO_NOT_AVAILABLE

    def get_would_take_again(self):
        """

        :return: teacher's percentage of would take again.
        """
        return self.take_again
