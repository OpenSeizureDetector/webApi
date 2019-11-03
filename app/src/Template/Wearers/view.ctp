<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Wearer $wearer
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('Edit Wearer'), ['action' => 'edit', $wearer->id]) ?> </li>
        <li><?= $this->Form->postLink(__('Delete Wearer'), ['action' => 'delete', $wearer->id], ['confirm' => __('Are you sure you want to delete # {0}?', $wearer->id)]) ?> </li>
        <li><?= $this->Html->link(__('List Wearers'), ['action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Wearer'), ['action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Datapoints'), ['controller' => 'Datapoints', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Datapoint'), ['controller' => 'Datapoints', 'action' => 'add']) ?> </li>
    </ul>
</nav>
<div class="wearers view large-9 medium-8 columns content">
    <h3><?= h($wearer->name) ?></h3>
    <table class="vertical-table">
        <tr>
            <th scope="row"><?= __('Name') ?></th>
            <td><?= h($wearer->name) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('User') ?></th>
            <td><?= $wearer->has('user') ? $this->Html->link($wearer->user->id, ['controller' => 'Users', 'action' => 'view', $wearer->user->id]) : '' ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Id') ?></th>
            <td><?= $this->Number->format($wearer->id) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Dob') ?></th>
            <td><?= h($wearer->dob) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Created') ?></th>
            <td><?= h($wearer->created) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Modified') ?></th>
            <td><?= h($wearer->modified) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Ald') ?></th>
            <td><?= $wearer->ald ? __('Yes') : __('No'); ?></td>
        </tr>
    </table>
    <div class="related">
        <h4><?= __('Related Datapoints') ?></h4>
        <?php if (!empty($wearer->datapoints)): ?>
        <table cellpadding="0" cellspacing="0">
            <tr>
                <th scope="col"><?= __('Id') ?></th>
                <th scope="col"><?= __('DataTime') ?></th>
                <th scope="col"><?= __('User Id') ?></th>
                <th scope="col"><?= __('Wearer Id') ?></th>
                <th scope="col"><?= __('AccMean') ?></th>
                <th scope="col"><?= __('AccSd') ?></th>
                <th scope="col"><?= __('Hr') ?></th>
                <th scope="col"><?= __('Category Id') ?></th>
                <th scope="col"><?= __('DataJSON') ?></th>
                <th scope="col"><?= __('Created') ?></th>
                <th scope="col"><?= __('Modified') ?></th>
                <th scope="col" class="actions"><?= __('Actions') ?></th>
            </tr>
            <?php foreach ($wearer->datapoints as $datapoints): ?>
            <tr>
                <td><?= h($datapoints->id) ?></td>
                <td><?= h($datapoints->dataTime) ?></td>
                <td><?= h($datapoints->user_id) ?></td>
                <td><?= h($datapoints->wearer_id) ?></td>
                <td><?= h($datapoints->accMean) ?></td>
                <td><?= h($datapoints->accSd) ?></td>
                <td><?= h($datapoints->hr) ?></td>
                <td><?= h($datapoints->category_id) ?></td>
                <td><?= h($datapoints->dataJSON) ?></td>
                <td><?= h($datapoints->created) ?></td>
                <td><?= h($datapoints->modified) ?></td>
                <td class="actions">
                    <?= $this->Html->link(__('View'), ['controller' => 'Datapoints', 'action' => 'view', $datapoints->id]) ?>
                    <?= $this->Html->link(__('Edit'), ['controller' => 'Datapoints', 'action' => 'edit', $datapoints->id]) ?>
                    <?= $this->Form->postLink(__('Delete'), ['controller' => 'Datapoints', 'action' => 'delete', $datapoints->id], ['confirm' => __('Are you sure you want to delete # {0}?', $datapoints->id)]) ?>
                </td>
            </tr>
            <?php endforeach; ?>
        </table>
        <?php endif; ?>
    </div>
</div>
