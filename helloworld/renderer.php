<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * renderer
 * @package     block
 * @subpackage  hello_world
 * @copyright   2017 benIT
 * @author      benIT <benoit.works@gmail.com>
 * @license     http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
defined('MOODLE_INTERNAL') || die;


class block_helloworld_renderer extends plugin_renderer_base
{
    /**
     * Defer to template.
     *
     * @param index_page $page
     *
     * @return string html for the page
     */
    public function render_countdown_page($page)
    {
        $data = $page->export_for_template($this);
        return parent::render_from_template('block_helloworld/countdown_page', $data);
    }

    public function render_gettoken_page($page)
    {
        $data = $page->export_for_template($this);
        return parent::render_from_template('block_helloworld/gettoken_page', $data);
    }
}

trait renderer_page_trait
{
    /** @var stdClass data to a template. */
    private $data;

    public function __construct($data)
    {
        $this->data = $data;
    }

    /**
     * Export this data so it can be used as the context for a mustache template.
     *
     * @return stdClass
     */
    public function export_for_template(renderer_base $output)
    {
        $data = new stdClass();
        return $this->data;
    }

}

class countdown_page implements renderable, templatable
{
    use renderer_page_trait;
}


class gettoken_page implements renderable, templatable
{
    use renderer_page_trait;
}