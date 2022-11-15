import os
import datetime
import uuid
import mysql.connector


class Database:
    def __init__(self, configparser):
        self._configparser = configparser

        self._create_mysql_connection()

        self._wp_posts_sql = "INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES "
        self._wp_posts_sql += "(1, %s, %s, %s, %s, '', 'pending', 'closed', 'closed', '', %s, '', '', %s, %s, '', 0, %s, 0, 'ad_post', '', 0)"

        self._wp_postmeta_sql = "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES "
        self._wp_postmeta_sql += "({id}, '_adforest_ad_status_', 'active'),"
        self._wp_postmeta_sql += "({id}, '_adforest_is_feature', '0'),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_currency', '$'),"
        self._wp_postmeta_sql += "({id}, '_adforest_poster_name', %s),"
        self._wp_postmeta_sql += "({id}, '_adforest_poster_contact', %s),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_location', %s),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_type', 'Sell'),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_condition', ''),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_warranty', ''),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_price', %s),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_map_lat', '40.7127837'),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_map_long', '-74.00594130000002'),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_bidding', ''),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_price_type', ''),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_bidding_date', ''),"
        self._wp_postmeta_sql += "({id}, '_adforest_ad_yvideo', ''),"
        self._wp_postmeta_sql += "({id}, '_thumbnail_id', %s),"
        self._wp_postmeta_sql += "({id}, 'sb_post_views_count', '0'),"
        self._wp_postmeta_sql += "({id}, '_sb_photo_arrangement_', %s)"

        self._wp_term_relationships_sql = "INSERT INTO `wp_term_relationships` (`object_id`, `term_taxonomy_id`, `term_order`) VALUES "
        # Category: Animals/Pets
        self._wp_term_relationships_sql += "({id}, {category_id}, 0),"
        # Type: Sell
        self._wp_term_relationships_sql += "({id}, 241, 0),"
        # Currency: $
        self._wp_term_relationships_sql += "({id}, 334, 0),"
        # Country: USA
        self._wp_term_relationships_sql += "({id}, 433, 0)"

        self._wp_posts_attachment_sql = "INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES "
        self._wp_posts_attachment_sql += "(1, %s, %s, '', %s, '', 'inherit', 'open', 'closed', '', %s, '', '', %s, %s, '', {id}, %s, 0, 'attachment', 'image/jpeg', 0)"

        self._wp_postmeta_attachment_sql = "INSERT INTO `wp_postmeta` (`post_id`, `meta_key`, `meta_value`) VALUES "
        self._wp_postmeta_attachment_sql += "({id}, '_wp_attached_file', %s)"

    def _create_mysql_connection(self):
        self._connection = mysql.connector.connect(
            host=self._configparser.database_host,
            user=self._configparser.database_username,
            passwd=self._configparser.database_password,
            database=self._configparser.database_name
        )

    def insert_data(self, data):
        cursor = self._connection.cursor()

        for element in data:
            cursor.execute(self._wp_posts_sql,
                           self._generate_wp_posts_data(element))
            wp_post_id = cursor.lastrowid

            images_ids = self._insert_images(element, wp_post_id, cursor)

            wp_postmeta_data = self._generate_wp_postmeta_data(
                element, wp_post_id, images_ids)
            cursor.execute(wp_postmeta_data[0], wp_postmeta_data[1])

            wp_term_relationships_sql_data = self._generate_wp_term_relationships_data(
                wp_post_id, element["title"], element["description"])
            cursor.execute(wp_term_relationships_sql_data)

        self._connection.commit()

    def _insert_images(self, element, wp_post_id, cursor):
        images_ids = []
        for index in range(4):
            imagename = element["image{0}".format(index+1)]
            if len(imagename) > 0:
                wp_posts_attachment_data = self._generate_wp_posts_attachment_data(
                    element, wp_post_id, imagename)
                cursor.execute(
                    wp_posts_attachment_data[0], wp_posts_attachment_data[1])
                images_ids.append(cursor.lastrowid)

                wp_postmeta_attachment_data = self._generate_wp_postmeta_attachment_data(
                    wp_post_id, imagename)
                cursor.execute(wp_postmeta_attachment_data)

        return images_ids

    def _generate_wp_posts_data(self, element):
        date = datetime.datetime.strptime(element["date"], "%B %d, %Y")
        date = date.strftime("%y-%m-%d %H:%M:%S")

        return (date,
                date,
                element["description"],
                element["title"],
                element["title"],
                date,
                date,
                "http://127.0.0.1/wordpress/ad/%s/" % uuid.uuid4().hex)

    def _generate_wp_postmeta_data(self, element, wp_post_id, images_ids):
        wp_postmeta_sql_id = self._wp_postmeta_sql.format(id=wp_post_id)

        thumbnail_id = images_ids[0]
        images_ids_string = str(images_ids).replace(" ", "")

        return (wp_postmeta_sql_id, (element["username"],
                                     element["phone"],
                                     element["address"],
                                     element["price"],
                                     thumbnail_id,
                                     images_ids_string))

    def _generate_wp_term_relationships_data(self, wp_post_id, title, description):
        category_id = self._get_category_id(title+" "+description)

        return self._wp_term_relationships_sql.format(
            id=wp_post_id, category_id=category_id)

    def _get_category_id(self, text):
        self._configparser.parse_categories()

        scores = [0] * 6
        scores[0] = self._count_category_score(
            self._configparser.auto_keywords, text)
        scores[1] = self._count_category_score(
            self._configparser.jobs_keywords, text)
        scores[2] = self._count_category_score(
            self._configparser.services_keywords, text)
        scores[3] = self._count_category_score(
            self._configparser.electronics_keywords, text)
        scores[4] = self._count_category_score(
            self._configparser.realestate_keywords, text)

        max_value = max(scores)
        if max_value == 0:
            return 346
        else:
            return self._list_id_to_category_id(scores.index(max_value))

    def _count_category_score(self, keywords, text):
        count = 0
        for keyword in keywords:
            if len(keyword) == 0:
                break

            count += text.lower().count(keyword.strip().lower())

        return count

    def _list_id_to_category_id(self, list_id):
        if list_id == 0:
            return 275
        elif list_id == 1:
            return 192
        elif list_id == 2:
            return 245
        elif list_id == 3:
            return 173
        elif list_id == 4:
            return 225
        else:
            return 346

    def _generate_wp_posts_attachment_data(self, element, wp_post_id, imagename):
        imagename_without_jpg = os.path.splitext(imagename)[0]
        date = datetime.datetime.strptime(element["date"], "%B %d, %Y")
        date = date.strftime("%y-%m-%d %H:%M:%S")

        wp_posts_attachment_sql_id = self._wp_posts_attachment_sql.format(
            id=wp_post_id)

        return (wp_posts_attachment_sql_id, (date,
                                             date,
                                             imagename_without_jpg,
                                             imagename_without_jpg,
                                             date,
                                             date,
                                             "http://127.0.0.1/wordpress/wp-content/uploads/facebook/{0}.jpg".format(imagename_without_jpg)))

    def _generate_wp_postmeta_attachment_data(self, wp_post_id, imagename):
        wp_postmeta_attachment_sql_id = self._wp_postmeta_attachment_sql.format(
            id=wp_post_id) % "'facebook/{0}'".format(imagename)

        return wp_postmeta_attachment_sql_id
