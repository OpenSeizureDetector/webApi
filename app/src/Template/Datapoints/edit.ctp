<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Datapoint $datapoint
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Form->postLink(
                __('Delete'),
                ['action' => 'delete', $datapoint->id],
                ['confirm' => __('Are you sure you want to delete # {0}?', $datapoint->id)]
            )
        ?></li>
        <li><?= $this->Html->link(__('List Datapoints'), ['action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Wearers'), ['controller' => 'Wearers', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Wearer'), ['controller' => 'Wearers', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Categories'), ['controller' => 'Categories', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Category'), ['controller' => 'Categories', 'action' => 'add']) ?></li>
    </ul>
</nav>
<div class="datapoints form large-9 medium-8 columns content">
    <?= $this->Form->create($datapoint) ?>
    <fieldset>
        <legend><?= __('Edit Datapoint') ?></legend>
        <?php
            echo $this->Form->control('dataTime', ['empty' => true]);
            echo $this->Form->control('user_id', ['options' => $users]);
            echo $this->Form->control('wearer_id', ['options' => $wearers]);
            echo $this->Form->control('accMean');
            echo $this->Form->control('accSd');
            echo $this->Form->control('hr');
            echo $this->Form->control('category_id', ['options' => $categories, 'empty' => true]);
            echo $this->Form->control('dataJSON');
        ?>
    </fieldset>
    <?= $this->Form->button(__('Submit')) ?>
    <?= $this->Form->end() ?>
</div>
