/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50724
Source Host           : 127.0.0.1:3306
Source Database       : novel_scrapy

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2020-09-30 15:18:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `n_cate`
-- ----------------------------
DROP TABLE IF EXISTS `n_cate`;
CREATE TABLE `n_cate` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '分类名称',
  `is_menu` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '是否菜单',
  `is_home` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '是否首页显示',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COMMENT='小说分类表';

-- ----------------------------
-- Records of n_cate
-- ----------------------------
INSERT INTO `n_cate` VALUES ('1', '玄幻奇幻', '1', '1', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('2', '武侠仙侠', '1', '1', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('3', '都市言情', '1', '1', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('4', '历史军事', '1', '1', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('5', '侦探推理', '1', '1', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('6', '网游竞技', '1', '0', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('7', '科幻灵异', '1', '0', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('8', '恐怖灵异', '1', '0', '2020-08-11 15:57:43', '2020-08-11 15:57:43');
INSERT INTO `n_cate` VALUES ('9', '其他类型', '1', '0', '2020-08-11 15:57:43', '2020-08-11 15:57:43');

-- ----------------------------
-- Table structure for `n_chapter`
-- ----------------------------
DROP TABLE IF EXISTS `n_chapter`;
CREATE TABLE `n_chapter` (
  `chapter_id` varchar(50) NOT NULL,
  `nov_id` varchar(50) NOT NULL DEFAULT '0' COMMENT '小说ID',
  `chapter_no` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '章节编号',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '章节标题',
  `desc` longtext NOT NULL COMMENT '章节内容',
  `link` varchar(100) NOT NULL DEFAULT '' COMMENT '章节采集链接',
  `source` varchar(10) NOT NULL DEFAULT '' COMMENT '章节采集站点源',
  `views` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '浏览次数',
  `text_num` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '章节字数',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '章节采集状态0正常，1失败',
  `try_views` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '采集重试次数',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`chapter_id`),
  KEY `udx_novid_no_source` (`nov_id`,`chapter_no`,`source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小说章节信息表';

-- ----------------------------
-- Records of n_chapter
-- ----------------------------

-- ----------------------------
-- Table structure for `n_novel`
-- ----------------------------
DROP TABLE IF EXISTS `n_novel`;
CREATE TABLE `n_novel` (
  `nov_id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '小说名称',
  `desc` varchar(2555) NOT NULL DEFAULT '' COMMENT '小说描述',
  `cover` varchar(100) NOT NULL DEFAULT '' COMMENT '小说封面',
  `cate_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '小说分类',
  `cate_name` varchar(30) NOT NULL DEFAULT '' COMMENT '分类名称',
  `author` varchar(30) NOT NULL DEFAULT '' COMMENT '小说作者',
  `views` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '浏览次数',
  `text_num` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '小说字数',
  `chapter_num` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '小说章节数',
  `chapter_updated_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最新章节时间',
  `chapter_id` varchar(50) NOT NULL DEFAULT '0' COMMENT '最新章节id',
  `chapter_title` varchar(100) NOT NULL DEFAULT '' COMMENT '最新章节标题',
  `collect_num` int(10) unsigned NOT NULL DEFAULT '0',
  `rec_num` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`nov_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小说主信息表';

-- ----------------------------
-- Records of n_novel
-- ----------------------------
